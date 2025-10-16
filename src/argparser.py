import argparse


class ArgParser:

    def __init__(self) -> None:
        lsParser = argparse.ArgumentParser(
            prog="ls",
            description="Show files and folders in current or specified folder",
        )
        lsParser.add_argument("-p", "--path", help="Set path", default=".")
        lsParser.add_argument(
            "-l",
            "--list",
            action="store_true",
            help="Show more information about files",
        )
        self.lsParser = lsParser

        cdParser = argparse.ArgumentParser(
            prog="cd", description="Change current directory"
        )
        cdParser.add_argument("path", help="New directory")
        self.cdParser = cdParser

        self.parsers = {"ls": self.lsParser, "cd": self.cdParser}

    def parse(self, cmd: str, args: list[str]) -> argparse.Namespace:
        return self.parsers[cmd].parse_args(args=args)
