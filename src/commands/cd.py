from pathlib import Path
import argparse

from src.logger import logger


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
            logger.warning('Invalid args: %s', ', '.join(unknown_args))

        path = f"{cwd}/{args.path}"
        return str(Path(path).resolve())
