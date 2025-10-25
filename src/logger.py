import logging


class Logger:

    def __init__(self) -> None:
        format = "[%(asctime)s] %(levelname)s: %(message)s"
        logging.basicConfig(
            level=logging.INFO,
            filename="t3000.log",
            datefmt="%Y/%m/%d %H:%M:%S",
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
