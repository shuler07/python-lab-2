from os import access, F_OK
from argparse import ArgumentParser

from src.errors import unknown_arguments_message, history_file_not_found_message


class History:

    def __init__(self) -> None:
        parser = ArgumentParser(
            prog="history", description="Show last executed commands"
        )
        parser.add_argument(
            "-c", "--count", help="Show certain amount of last commands"
        )
        self.parser = parser

    def execute(self, _args: list[str]) -> None:
        args, unknown_args = self.parser.parse_known_args(args=_args)
        if len(unknown_args) > 0:
            unknown_arguments_message(unknown_args=unknown_args)

        count = int(args.count) if args.count else 5

        if not access(path="./.history", mode=F_OK):
            history_file_not_found_message()
            return

        for line in open(file="./.history").readlines():
            if count > 0:
                print(line.rstrip())
                count -= 1
        self.write(cmd=f"history --count {args.count if args.count else 5}")

    def write(self, cmd: str) -> None:
        if access(path="./.history", mode=F_OK):
            lines_count = len(open(file="./.history").readlines())
            with open(file="./.history", mode="a") as f:
                f.write(f"({lines_count + 1}) {cmd}\n")
        else:
            with open(file="./.history", mode="x") as f:
                f.write(f"(1) {cmd}\n")

    def mark_undone(self, n: int) -> None:
        lines = open(file="./.history").readlines()
        with open(file="./.history", mode="w") as f:
            for i, line in enumerate(lines, start=1):
                if i != n:
                    f.write(line)
                else:
                    f.write(f"{line.rstrip()} (undone)\n")


cmd_history = History()
