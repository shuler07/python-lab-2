from os import access, F_OK, mkdir
from os.path import isabs, isdir, isfile
from pathlib import Path
from shutil import move, rmtree
from argparse import ArgumentParser, ArgumentError

from src.commands.history import cmd_history
from src.errors import (
    path_doesnt_exist_message,
    missing_required_arguments_message,
    unknown_arguments_message,
    path_leads_to_dir_instead_of_file_message,
    path_leads_to_file_instead_of_dir_message,
    attempt_to_remove_parent_path_message,
)


class Rm:

    def __init__(self) -> None:
        parser = ArgumentParser(
            prog="rm", description="Remove file or folder", exit_on_error=False
        )
        parser.add_argument("path", help="Path to file or folder to delete")
        parser.add_argument(
            "-r",
            "--recursive",
            action="store_true",
            help="Delete folder with all including",
        )
        self.parser = parser

    def execute(self, cwd: str | None, _args: list[str]) -> None:
        try:
            args, unknown_args = self.parser.parse_known_args(args=_args)
        except ArgumentError as e:
            missing_args = e.message[e.message.index(":") + 2 :]
            missing_required_arguments_message(missing_args_str=missing_args)
            return

        if len(unknown_args) > 0:
            unknown_arguments_message(unknown_args=unknown_args)

        path = str(
            Path(args.path if isabs(args.path) else f"{cwd}\{args.path}").resolve()
        )
        if not access(path=path, mode=F_OK):
            path_doesnt_exist_message(path=path)
            return
        if cwd and str(path) in cwd:
            attempt_to_remove_parent_path_message(path=path)
            return

        if not access(path="./.trash", mode=F_OK):
            mkdir("./.trash")

        if args.recursive:
            if isfile(path):
                path_leads_to_file_instead_of_dir_message(path=path)
                return

            move(src=path, dst="./.trash")
            if cwd:
                cmd_history.write(cmd=f"rm {path} --recursive")
        else:
            if isdir(path):
                path_leads_to_dir_instead_of_file_message(path=path)
                return

            move(src=path, dst="./.trash")
            if cwd:
                cmd_history.write(cmd=f"rm {path}")

    def clear_trash(self) -> None:
        if access(path="./.trash", mode=F_OK):
            rmtree("./.trash")


cmd_rm = Rm()
