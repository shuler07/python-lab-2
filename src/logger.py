import logging

from src.constants import DATETIME_FORMAT


class Logger:
    "Basic logger for Terminal3000. Logs into t3000.log"

    def __init__(self) -> None:
        format = "[%(asctime)s] %(levelname)s: %(message)s"
        logging.basicConfig(
            level=logging.INFO,
            filename="t3000.log",
            datefmt=DATETIME_FORMAT,
            format=format,
        )
        self.logger = logging.getLogger("t3000.log")

    def info(self, msg: str, *args) -> None:
        self.logger.info(msg, *args)

    def warning(self, msg: str, *args) -> None:
        self.logger.warning(msg, *args)

    def error(self, msg: str, *args) -> None:
        self.logger.error(msg, *args)


logger = Logger()
