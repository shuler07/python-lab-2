from os import access, F_OK
from argparse import ArgumentParser
from datetime import datetime

from src.errors import unknown_arguments_message, history_file_not_found_message
from src.constants import DATETIME_FORMAT


class History:
    "'history' command to read file contents"

    def __init__(self) -> None:
        parser = ArgumentParser(
            prog="history", description="Show last executed commands"
        )
        parser.add_argument(
            "-c", "--count", help="Show certain amount of last commands"
        )
        self.parser = parser
        self.initiated = False  # To write 'New session' at session start
        self.count = 1  # To write command number in current session

    def execute(self, _args: list[str]) -> None:
        """
        Execute 'history' command from given directory with given args
        Args:
            cwd (str): directory to execute from
            _args (list[str]): args for 'history' command
        """
        args, unknown_args = self.parser.parse_known_args(args=_args)
        if len(unknown_args) > 0:
            unknown_arguments_message(unknown_args=unknown_args)

        # Default count of commands to be printed
        count = int(args.count) if args.count else 5

        if not access(path="./.history", mode=F_OK):
            history_file_not_found_message()
            return

        for line in open(file="./.history").readlines():
            if count > 0:
                print(line.rstrip())  # Need cause of empty lines between prints
                count -= 1
        self.write(cmd=f"history --count {args.count if args.count else 5}")

    def write(self, cmd: str) -> None:
        """
        Write to .history command
        Args:
            cmd (str): command to be written
        """
        if access(path="./.history", mode=F_OK):
            with open(file="./.history", mode="a") as f:  # Append to existing file
                if not self.initiated:
                    date = datetime.strftime(datetime.now(), format=DATETIME_FORMAT)
                    f.write(f"\nNew session {date}\n")
                    self.initiated = True

                f.write(f"({self.count}) {cmd}\n")
                self.count += 1
        else:
            with open(file="./.history", mode="x") as f:  # Initialize new file
                if not self.initiated:
                    date = datetime.strftime(datetime.now(), format=DATETIME_FORMAT)
                    f.write(f"\nNew session {date}\n")
                    self.initiated = True

                f.write(f"(1) {cmd}\n")
                self.count = 2

    def mark_undone(self, line: int) -> None:
        """
        Mark command as undone
        Args:
            line (int): line index of command to be undone
        """
        lines = open(file="./.history").readlines()
        with open(file="./.history", mode="w") as f:
            for _line, cmd in enumerate(lines):
                if _line != line:
                    f.write(cmd)
                else:
                    f.write(f"{cmd.rstrip()} (undone)\n")
                    break


cmd_history = History()
