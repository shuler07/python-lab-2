from os import access, F_OK
from os.path import isabs
from pathlib import Path
from tarfile import TarFile, is_tarfile
from argparse import ArgumentParser, ArgumentError

from src.commands.history import cmd_history
from src.errors import (
    path_doesnt_exist_message,
    missing_required_arguments_message,
    unknown_arguments_message,
    path_doesnt_lead_to_tarfile_message,
)


class Untar:

    def __init__(self):
        parser = ArgumentParser(
            prog="untar", description="Untar archive to folder", exit_on_error=False
        )
        parser.add_argument("path", help="Path to tar archive")
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

        if not is_tarfile(name=path):
            path_doesnt_lead_to_tarfile_message(path=path)
            return

        with TarFile(name=path, mode="r") as zipr:
            zipr.extractall()
        cmd_history.write(cmd=f"untar {path}")


cmd_untar = Untar()
