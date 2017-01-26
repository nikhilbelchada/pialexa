import sys
from console_helper import ConsoleHelper


if __name__ == "__main__":
    import logging
    from logging.config import fileConfig

    fileConfig('logger_config.ini')
    logger = logging.getLogger()
    logger.info('Starting PiAlexa Service')

    SENSE_HAT = 0
    CONSOLE = 1

    option = SENSE_HAT
    if len(sys.argv) > 1 and int(sys.argv[1]) == CONSOLE:
        option = CONSOLE

    if option == CONSOLE:
        logger.info('Welcome to Console Alexa')
        while True:
            console_input = raw_input('Press any key to ask question (q to quit)')
            console_helper = ConsoleHelper()
            if console_input == 'q':
                logger.info('Thankyou for trying Console Alexa, Hope you enjoyed it!!')
                sys.exit()
            else:
                console_helper.record()
                console_helper.process()
    else:
        from sensehat_helper import SenseHatHelper
        sense_object = SenseHatHelper()
        sense_object.sense_hat.show_letter("?")
        logger.info('Welcome to Pi Alexa')

        try:
            while True:
                pass
        except KeyboardInterrupt:
            sense_object.sense_hat.clear()
            logger.info('Thankyou for trying PiAlexa, Hope you enjoyed it!!')
