from os import access, F_OK
from os.path import isfile, isabs
from pathlib import Path
from argparse import ArgumentParser, ArgumentError

from src.commands.history import cmd_history
from src.errors import (
    path_doesnt_exist_message,
    unknown_arguments_message,
    missing_required_arguments_message,
    path_leads_to_file_instead_of_dir_message,
)


class Cd:

    def __init__(self) -> None:
        parser = ArgumentParser(
            prog="cd", description="Change current directory", exit_on_error=False
        )
        parser.add_argument("path", help="Directory path")
        self.parser = parser

    def execute(self, cwd: str, _args: list[str]) -> str:
        try:
            args, unknown_args = self.parser.parse_known_args(args=_args)
        except ArgumentError as e:
            missing_args = e.message[e.message.index(":") + 2 :]
            missing_required_arguments_message(missing_args_str=missing_args)
            return str(Path(cwd).resolve())

        if len(unknown_args) > 0:
            unknown_arguments_message(unknown_args=unknown_args)

        if args.path == "~":
            path = str(Path().home().resolve())
            cmd_history.write(cmd=f"cd {path}")
            return path

        path = str(
            Path(args.path if isabs(args.path) else f"{cwd}\{args.path}").resolve()
        )
        if isfile(path):
            path_leads_to_file_instead_of_dir_message(path=path)
            return str(Path(cwd).resolve())
        if not access(path=path, mode=F_OK):
            path_doesnt_exist_message(path=path)
            return str(Path(cwd).resolve())

        return path


cmd_cd = Cd()
