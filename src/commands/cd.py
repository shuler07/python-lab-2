from pathlib import Path
import argparse
from os import access, F_OK

from src.logger import logger
from src.colortext import colorize


class Cd:

    def __init__(self) -> None:
        parser = argparse.ArgumentParser(
            prog="cd", description="Change current directory"
        )
        parser.add_argument("path", help="New directory")
        self.parser = parser

    def execute(self, cwd: str, _args: list[str]) -> str:
        args, unknown_args = self.parser.parse_known_args(args=_args)
        if len(unknown_args) > 0:
            logger.warning("Invalid args: %s", ", ".join(unknown_args))

        path = f"{cwd}\{args.path}"
        if not access(path=path, mode=F_OK):
            logger.warning("Path %s doesn't exist", path)
            msg1 = colorize(text="Path", color="red")
            msg2 = colorize(text=path, color="red", bold=True)
            msg3 = colorize(text="doesn't exist", color="red")
            print(msg1, msg2, msg3, sep=" ")
            return str(Path(cwd).resolve())

        return str(Path(path).resolve())
