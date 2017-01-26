import logging
from alexa_service import AlexaService
from alsa_helper import AlsaHelper
from utils import FileHelper


logger = logging.getLogger()


class ConsoleHelper(object):
    def __init__(self):
        self.audio = ''

        # Check Audio Device
        self.alsa_helper = AlsaHelper()

    def record(self):
        self.audio = ''
        self.alsa_helper.set_alsa_input()

        total = 0
        while total < AlsaHelper.RECORDING_LIMIT:
            total += 1
            l, data = self.alsa_helper.alsa_input.read()
            if l:
                self.audio += data

    def process(self):
        """Voice data is dumped on file and then passed to alexa service for
        processing"""
        logger.info('Submitting Voice data to Alexa Service for processing')
        FileHelper.save(self.audio)

        # pass voice data to alexa service
        success = AlexaService().post_voice_data()

        # reset data
        self.alsa_helper.alsa_input = None
        self.audio = ''
