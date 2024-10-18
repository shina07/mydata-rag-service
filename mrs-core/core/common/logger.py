import logging
import sys
from typing import Final

FORMAT: Final[str] = '%(levelname)s: %(asctime)s|[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s'
DATEFMT: Final[str] = '%Y-%m-%d %H:%M:%S %Z'


class Logger:
    @staticmethod
    def get_logger(name, level=logging.INFO):
        return Logger._setup_logger(name, level=level)

    @staticmethod
    def _setup_logger(filename, level=logging.INFO):
        logging.basicConfig(
            format=FORMAT,
            datefmt=DATEFMT,
            stream=sys.stdout
        )

        logger = logging.getLogger(filename)
        logger.setLevel(level=level)

        return logger
