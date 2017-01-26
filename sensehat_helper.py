import os
import wave
import logging
import alsaaudio
try:
    from sense_hat import SenseHat
except ImportError:
    raise ValueError('You are not on RaspberryPi, try "python start.py 1"')
from alexa_service import AlexaService
from alsa_helper import AlsaHelper
from utils import FileHelper


path = os.path.realpath(__file__).rstrip(os.path.basename(__file__))
logger = logging.getLogger()


class SenseHatHelper(object):
    DEVICE_NAME = "Raspberry Pi Sense HAT Joystick"
    DIRECTION_MIDDLE = 'middle'
    ACTION_PRESSED = 'pressed'
    ACTION_RELEASED = 'released'
    ACTION_HELD = 'held'

    def __init__(self):
        self.audio = ''

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
        self.alsa_helper = AlsaHelper()

    def handle_button_released(self):
        """Voice data is dumped on file and then passed to alexa service for
        processing"""
        logger.info('Submitting Voice data to Alexa Service for processing')
        FileHelper.save(self.audio)

        # pass voice data to alexa service
        self.sense_hat.show_letter("P")
        success = AlexaService().post_voice_data()

        # reset data
        self.alsa_helper.alsa_input = None
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
        self.alsa_helper.set_alsa_input()

        l, data = self.alsa_helper.alsa_input.read()
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
