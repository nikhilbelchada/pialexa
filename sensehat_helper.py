import wave
import numpy
import alsaaudio
from evdev import (
    list_devices,
    InputDevice,
    ecodes,
)
from sense_hat import SenseHat


path = os.path.realpath(__file__).rstrip(os.path.basename(__file__))


class SenseHatHelper(object):
    SOUND_CARD = "plughw:1"  # arecord -L
    FILE_NAME = 'voice.wav'
    DEVICE_NAME = "Raspberry Pi Sense HAT Joystick"
    KEY_RELEASED = 0
    KEY_PRESSED = 1
    KEY_HELD = 2

    def __init__(self):
        self.audio = ''
        # check sense hat is attached
        try:
            self.sense_hat = SenseHat()
        except Exception as e:
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

        # send data to alexa service

        # reset data
        self.alsa_input = None
        self.audio = ''

    def handle_button_hold(self):
        """Voice data is recorded"""
        l, data = self.alsa_input.read()
        if l:
            self.audio += data
            audio = numpy.formatstring(data, type='int16')
            loudness = int(numpy.abs(a).mean())

    def handle_button_press(self):
        """Initiate Audio Recording"""
        self.audio = ''
        self.alsa_input.setchannels(1)
        self.alsa_input.setrate(16000)
        self.alsa_input.setformat(alsaaudio.PCM_FORMAT_S16_LE)
        self.alsa_input.setperiodsize(1024)

        l, data = self.alsa_input.read()
        if l:
            self.audio += data

    def handle_key_press_event(self, key):
        """Routes JoyStick key event to appropriate action"""
        if key == self.KEY_RELEASED:
            self.handle_button_released()
        elif key == self.KEY_PRESSED:
            self.handle_button_press()
        elif key == self.KEY_HELD:
            self.handle_button_hold()
        else:
            print 'Press Joystick to record'

    def start_event_loop(self):
        """Start event loop and listen to sense hat key events, to perform
        key based action
        """
        for event in self.device.read_loop():
            if event.type == ecodes.EV_KEY and event.code == ecodes.KEY_ENTER:
                self.handle_key_press_event(event.value)
