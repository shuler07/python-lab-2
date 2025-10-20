from os import access, F_OK
from os.path import isabs
from zipfile import ZipFile, is_zipfile
from argparse import ArgumentParser, ArgumentError

from src.errors import (
    path_doesnt_exist_message,
    missing_required_arguments_message,
    unknown_arguments_message,
    path_doesnt_lead_to_zipfile_message,
)


class Unzip:

    def __init__(self):
        parser = ArgumentParser(
            prog="unzip", description="Unzip archive to folder", exit_on_error=False
        )
        parser.add_argument("path", help="Path to zip archive")
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

        path = args.path if not isabs(args.path) else f"{cwd}\{args.path}"
        if not access(path=path, mode=F_OK):
            path_doesnt_exist_message(path=path)
            return

        if not is_zipfile(filename=path):
            path_doesnt_lead_to_zipfile_message(path=path)
            return

        with ZipFile(file=path, mode="r") as zipr:
            zipr.extractall()
