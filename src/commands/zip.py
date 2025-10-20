from os import access, F_OK, walk
from os.path import isabs, isfile, join
from zipfile import ZipFile
from argparse import ArgumentParser, ArgumentError

from src.errors import (
    path_doesnt_exist_message,
    missing_required_arguments_message,
    unknown_arguments_message,
    path_leads_to_file_instead_of_dir_message,
)


class Zip:

    def __init__(self):
        parser = ArgumentParser(
            prog="zip",
            description="Create zip archive from folder",
            exit_on_error=False,
        )
        parser.add_argument("path", help="Path to folder to zip")
        parser.add_argument("name", help="Zip archive name")
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

        if isfile(path):
            path_leads_to_file_instead_of_dir_message(path=path)
            return

        zipname = args.name if args.name.endswith(".zip") else f"{args.name}.zip"
        with ZipFile(file=zipname, mode="w") as zipw:
            for root, _, files in walk(top=path):
                for file in files:
                    filepath = join(root, file)
                    zipw.write(filename=filepath)
