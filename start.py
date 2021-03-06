import sys
from console_helper import ConsoleHelper
from pialexa import settings


if __name__ == "__main__":
    import logging
    from logging.config import fileConfig

    fileConfig('logger_config.ini')
    logger = logging.getLogger()
    if not (settings.CLIENT_ID and settings.CLIENT_SECRET):
        logger.warning('Please run "source setup.sh" first')
        sys.exit()

    logger.info('Starting PiAlexa Service')

    SENSE_HAT = 0
    CONSOLE = 1

    option = SENSE_HAT
    if len(sys.argv) > 1 and int(sys.argv[1]) == CONSOLE:
        option = CONSOLE

    if option == CONSOLE:
        logger.info('Welcome to Console Alexa')
        while True:
            console_input = raw_input(
                'Enter c to ask question (any other key to quit)')
            console_helper = ConsoleHelper()

            if console_input == 'c':
                console_helper.record()
                console_helper.process()
            else:
                logger.info(
                    'Thankyou for trying Console Alexa, Hope you enjoyed it!!')
                sys.exit()
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
