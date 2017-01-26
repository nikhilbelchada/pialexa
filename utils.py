import os
import wave

path = os.path.realpath(__file__).rstrip(os.path.basename(__file__))


class FileHelper(object):
    """Helper Class to save audio data to file"""
    FILE_NAME = 'voice.wav'
    CHANNELS = 1
    FRAME_RATE = 16000
    SAMPLE_WIDTH = 2

    @classmethod
    def save(cls, audio, channels=CHANNELS, framerate=FRAME_RATE,
             sample_width=SAMPLE_WIDTH):
        wave_object = wave.open(path + cls.FILE_NAME, 'w')
        wave_object.setnchannels(channels)
        wave_object.setframerate(framerate)
        wave_object.setsampwidth(sample_width)
        wave_object.writeframes(audio)
        wave_object.close()
