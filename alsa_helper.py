import logging
import alsaaudio


logger = logging.getLogger()


class AlsaHelper(object):
    SOUND_CARD = "plughw:1"  # arecord -L
    CHANNELS = 1
    RECORDING_LIMIT = 30  # Equivialent to ~ 5 sec, Used in console mode

    # You will have to set these below value based on Micorphone
    # PERIOD_SIZE = 1024  - Specific to PI
    PERIOD_SIZE = 2
    # RATE = 16000  - Specific to PI
    RATE = 8500

    def __init__(self):
        self.alsa_input = None
        self.set_alsa_input()

    def set_alsa_input(self):
        """Helper function to connect to Micorphone"""
        try:
            if not self.alsa_input:
                self.alsa_input = alsaaudio.PCM(alsaaudio.PCM_CAPTURE,
                                                alsaaudio.PCM_NORMAL,
                                                self.SOUND_CARD)

            self.alsa_input.setchannels(self.PERIOD_SIZE)
            self.alsa_input.setrate(self.RATE)
            self.alsa_input.setformat(alsaaudio.PCM_FORMAT_S16_LE)
            self.alsa_input.setperiodsize(self.PERIOD_SIZE)

            logger.info('Microphone is ready!')
        except alsaaudio.ALSAAudioError:
            logger.exception('Microphone not found')
            raise IOError('Microphone not found')
