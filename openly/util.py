import logging


def setupLogger(name: str = __file__, level: int = logging.DEBUG):
    logger = logging.getLogger(name or __name__)
    logger.setLevel(logging.DEBUG)

    handler = logging.StreamHandler()
    handler.setLevel(level=level)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    return logger
