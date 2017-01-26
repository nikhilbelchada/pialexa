import os
import wave
import logging
import alsaaudio
from sense_hat import SenseHat
from alexa_service import AlexaService


path = os.path.realpath(__file__).rstrip(os.path.basename(__file__))
logger = logging.getLogger()


class SenseHatHelper(object):
    SOUND_CARD = "plughw:1"  # arecord -L
    FILE_NAME = 'voice.wav'
    DEVICE_NAME = "Raspberry Pi Sense HAT Joystick"
    DIRECTION_MIDDLE = 'middle'
    ACTION_PRESSED = 'pressed'
    ACTION_RELEASED = 'released'
    ACTION_HELD = 'held'

    def __init__(self):
        self.audio = ''
        self.alsa_input = None

        # check sense hat is attached
        try:
            self.sense_hat = SenseHat()
            self.sense_hat.stick.direction_middle = self.handle_key_press_event
            self.status = ''

            logger.info('Sense Hat is ready!')
        except Exception as e:
            raise logger.exception('SenseHat device not found')
            raise IOError('Seems sense hat is not attached!')

        # Check Audio Device
        self.set_alsa_input()

    def set_alsa_input(self):
        """Helper function to connect to Micorphone"""
        try:
            if not self.alsa_input:
                self.alsa_input = alsaaudio.PCM(alsaaudio.PCM_CAPTURE,
                                                alsaaudio.PCM_NORMAL,
                                                self.SOUND_CARD)

            self.alsa_input.setchannels(1)
            self.alsa_input.setrate(16000)
            self.alsa_input.setformat(alsaaudio.PCM_FORMAT_S16_LE)
            self.alsa_input.setperiodsize(1024)

            logger.info('Microphone is ready!')
        except alsaaudio.ALSAAudioError:
            logger.exception('Microphone not found')
            raise IOError('Microphone not found')

    def handle_button_released(self):
        """Voice data is dumped on file and then passed to alexa service for
        processing"""
        logger.info('Submitting Voice data to Alexa Service for processing')
        
        wave_object = wave.open(path + self.FILE_NAME, 'w')
        wave_object.setnchannels(1)
        wave_object.setframerate(16000)
        wave_object.setsampwidth(2)
        wave_object.writeframes(self.audio)
        wave_object.close()

        # pass voice data to alexa service
        self.sense_hat.show_letter("P")
        success = AlexaService().post_voice_data()

        # reset data
        self.alsa_input = None
        self.audio = ''

        if success:
            self.sense_hat.show_letter("?")
        else:
            self.sense_hat.show_letter("E")

    def handle_button_hold(self):
        """Voice data is recorded"""
        l, data = self.alsa_input.read()
        if l:
            self.audio += data

    def handle_button_press(self):
        """Initiate Audio Recording"""

        self.audio = ''
        self.set_alsa_input()

        l, data = self.alsa_input.read()
        if l:
            self.audio += data

    def handle_key_press_event(self, event):
        """Routes JoyStick key event to appropriate action"""

        if event.action == self.ACTION_RELEASED:
            self.handle_button_released()
        elif event.action == self.ACTION_PRESSED:
            self.sense_hat.clear()
            self.sense_hat.show_letter("R")
            self.handle_button_press()
        elif event.action == self.ACTION_HELD:
            self.handle_button_hold()
