from os import access, F_OK
from os.path import isdir, isabs
from argparse import ArgumentParser, ArgumentError

from src.errors import (
    path_doesnt_exist_message,
    unknown_arguments_message,
    missing_required_arguments_message,
    path_leads_to_dir_instead_of_file_message,
    permission_denied_message,
)


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
            missing_required_arguments_message(missing_args_str=missing_args)
            return

        if len(unknown_args) > 0:
            unknown_arguments_message(unknown_args=unknown_args)

        path = args.path if isabs(args.path) else f"{cwd}\{args.path}"
        if not access(path=path, mode=F_OK):
            path_doesnt_exist_message(path=path)
            return

        if isdir(path):
            path_leads_to_dir_instead_of_file_message(path=path)
            return

        try:
            for line in open(path):
                print(line.rstrip("\n"))
        except PermissionError:
            permission_denied_message(path=path)
