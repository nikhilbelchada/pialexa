from sensehat_helper import SenseHatHelper


if __name__ == "__main__":
    import logging
    from logging.config import fileConfig

    fileConfig('logger_config.ini')
    logger = logging.getLogger()
    logger.info('Starting PiAlexa Service')

    sense_object = SenseHatHelper()
    sense_object.sense_hat.show_letter("?")
    logger.info('Welcome to Pi Alexa')

    try:
        while True:
            pass
    except KeyboardInterrupt:
        sense_object.sense_hat.clear()
        logger.info('Thankyou for trying PiAlexa, Hope you enjoyed it!!')
