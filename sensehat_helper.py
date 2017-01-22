import os
import wave
import alsaaudio
from evdev import (
    list_devices,
    InputDevice,
    ecodes,
)
from sense_hat import SenseHat
from alexa_service import AlexaService


path = os.path.realpath(__file__).rstrip(os.path.basename(__file__))


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

        # check sense hat is attached
        try:
            self.sense_hat = SenseHat()
            self.sense_hat.stick.direction_middle = self.handle_key_press_event
            self.status = ''
        except Exception as e:
            print '====', e
            raise IOError('Seems sense hat is not attached!')

        # Check Audio Device
        try:
            self.alsa_input = alsaaudio.PCM(alsaaudio.PCM_CAPTURE,
                                            alsaaudio.PCM_NORMAL,
                                            self.SOUND_CARD)
        except alsaaudio.ALSAAudioError:
            raise IOError('Microphone not found')

    def handle_button_released(self):
        """Voice data is dumped on file and then passed to alexa service for
        processing"""
        
        wave_object = wave.open(path + self.FILE_NAME, 'w')
        wave_object.setnchannels(1)
        wave_object.setframerate(16000)
        wave_object.setsampwidth(2)
        wave_object.writeframes(self.audio)
        wave_object.close()

        # pass voice data to alexa service
        self.sense_hat.show_letter("P")
        AlexaService().post_voice_data()

        # reset data
        self.audio = ''
        self.sense_hat.show_letter("?")

    def handle_button_hold(self):
        """Voice data is recorded"""
        print "Your voice is being recorded, contiue to hold the button"

        l, data = self.alsa_input.read()
        if l:
            self.audio += data

    def handle_button_press(self):
        """Initiate Audio Recording"""
        print "Voice has been recorded and is being processed"

        self.audio = ''
        self.alsa_input.setchannels(1)
        self.alsa_input.setrate(16000)
        self.alsa_input.setformat(alsaaudio.PCM_FORMAT_S16_LE)
        self.alsa_input.setperiodsize(1024)

        l, data = self.alsa_input.read()
        if l:
            self.audio += data

    def handle_key_press_event(self, event):
        """Routes JoyStick key event to appropriate action"""
        print "You hit SenseHAT middle button"

        if event.action == self.ACTION_RELEASED:
            self.handle_button_released()
        elif event.action == self.ACTION_PRESSED:
            self.sense_hat.clear()
            self.sense_hat.show_letter("R")
            self.handle_button_press()
        elif event.action == self.ACTION_HELD:
            self.handle_button_hold()
