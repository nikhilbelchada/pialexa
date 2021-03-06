"""
Module to take care of Alexa Request and Response
"""
import re
import os
import json
import logging
import requests
from pialexa.utils import Credential
from pialexa import settings
from utils import FileHelper


path = os.path.realpath(__file__).rstrip(os.path.basename(__file__))
logger = logging.getLogger()


class AlexaService(object):
    """Helper class to post voice data to Alexa Service and
    play the alexa response

    Also, when necessary it auto refreshes Alexa Token
    """
    FILE_NAME = 'response.mp3'

    def __init__(self):
         try:
             data = Credential().data
             self.refresh_token = data['refresh_token']
             self.token = data.get('token', None)
         except KeyError:
             logger.exception('Run web server to get refresh token')
             raise ValueError('Run web server to get refresh token')

         self.get_token()

    def get_token(self):
        """Get already persisted token, else fetches the token from
        amazon and store it for later request"""
        if self.token:
            return self.token

        payload = {
            "client_id": settings.CLIENT_ID,
            "client_secret": settings.CLIENT_SECRET,
            "refresh_token": self.refresh_token,
            "grant_type": "refresh_token"
        }

        response = requests.post(settings.AMAZON_TOKEN_URL, data=payload)
        self.token = json.loads(response.text)['access_token']

        Credential().dump({'token': self.token})

    def post_voice_data(self):
        """Helper function to post recorded voice data to alexa service
        and play the audio response from alexa

        Returns:
            bool: True is 200 response from alexa service else False
        """
        headers = {'Authorization' : 'Bearer %s' % self.token}
        d = {
            "messageHeader": {
                "deviceContext": [
                    {
                        "name": "playbackState",
                        "namespace": "AudioPlayer",
                        "payload": {
                            "streamId": "",
                            "offsetInMilliseconds": "0",
                            "playerActivity": "IDLE"
                        }
                    }
                ]
            },
            "messageBody": {
                "profile": "alexa-close-talk",
                "locale": "en-us",
                "format": "audio/S16; rate=16000; channels=1"
            }
        }

        with open(path + FileHelper.FILE_NAME) as inf:
            files = [
                ('file', ('request', json.dumps(d),
                          'application/json; charset=UTF-8')),
                ('file', ('audio', inf, 'audio/S16; rate=16000; channels=1'))
            ]

            response = requests.post(settings.AMAZON_ALEXA_VOICE_URL,
                                     headers=headers, files=files)

            if response.status_code == 200:
                logger.info('Successfull Response from Alexa Service')

                for v in response.headers['content-type'].split(";"):
                    if re.match('.*boundary.*', v):
                        boundary =  v.split("=")[1]

                data = response.content.split(boundary)

                for content in data:
                    if (len(content) >= 1024):
                        audio = content.split('\r\n\r\n')[1].rstrip('--')

                with open(path + self.FILE_NAME, 'wb') as file_object:
                    file_object.write(audio)
                    os.system('mpg123 -q {0}{1}'.format(path, self.FILE_NAME))

                return True

            if response.status_code == 403:
                logger.warning('Token exipred, Refreshing Token')
                # Refresh and set the token
                self.token = None
                self.get_token()

                return False
            if response.status_code == 204:
                logger.warning('Provided Voice data is either empty or blank')
                return False
