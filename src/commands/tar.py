from os import access, F_OK, walk
from os.path import isabs, isfile, join
from pathlib import Path
from tarfile import TarFile
from argparse import ArgumentParser, ArgumentError

from src.commands.history import cmd_history
from src.errors import (
    path_doesnt_exist_message,
    missing_required_arguments_message,
    unknown_arguments_message,
    path_leads_to_file_instead_of_dir_message,
)


class Tar:

    def __init__(self):
        parser = ArgumentParser(
            prog="tar",
            description="Create tar archive from folder",
            exit_on_error=False,
        )
        parser.add_argument("path", help="Path to folder to tar")
        parser.add_argument("name", help="Tar archive name")
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

        path = str(
            Path(args.path if not isabs(args.path) else f"{cwd}\{args.path}").resolve()
        )
        if not access(path=path, mode=F_OK):
            path_doesnt_exist_message(path=path)
            return

        if isfile(path):
            path_leads_to_file_instead_of_dir_message(path=path)
            return

        tarname = args.name if args.name.endswith(".tar") else f"{args.name}.tar"
        with TarFile(name=tarname, mode="w") as zipw:
            for root, _, files in walk(top=path):
                for file in files:
                    filepath = join(root, file)
                    zipw.add(name=filepath)
        cmd_history.write(cmd=f"tar {path} {tarname}")


cmd_tar = Tar()
