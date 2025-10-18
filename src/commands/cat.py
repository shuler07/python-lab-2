from os import access, F_OK
from argparse import ArgumentParser, ArgumentError

from src.logger import logger
from src.colortext import colorize


class Cat:

    def __init__(self) -> None:
        parser = ArgumentParser(
            prog="cat", description="Output file contents", exit_on_error=False
        )
        parser.add_argument("path", help="File path")
        self.parser = parser

    def execute(self, cwd: str, _args: list[str]) -> None:
        try:
            args, unknown_args = self.parser.parse_known_args(args=_args)
        except ArgumentError as e:
            missing_args = e.message[e.message.index(":") + 2 :]
            logger.error("Missing required arguments: %s", missing_args)
            msg1 = colorize(text="Missing required arguments:", color="red")
            msg2 = colorize(text=missing_args, color="red", bold=True)
            print(msg1, msg2, sep=" ")
            return

        if len(unknown_args) > 0:
            logger.warning("Invalid args: %s", ", ".join(unknown_args))

        path = f"{cwd}\{args.path}"
        if not access(path=path, mode=F_OK):
            logger.warning('Path "%s" doesn\'t exist', path)
            msg1 = colorize(text="Path", color="red")
            msg2 = colorize(text=path, color="red", bold=True)
            msg3 = colorize(text="doesn't exist", color="red")
            print(msg1, msg2, msg3, sep=" ")
            return

        try:
            with open(path) as f:
                for line in f:
                    print(line.rstrip("\n"))
        except PermissionError:
            logger.error('Directory path received instead of file path: "%s"', path)
            msg1 = colorize(
                text="Directory path received instead of file path:", color="red"
            )
            msg2 = colorize(text=path, color="red", bold=True)
            print(msg1, msg2, sep=" ")
