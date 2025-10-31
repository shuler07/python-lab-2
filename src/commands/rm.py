from os import mkdir, remove
from os.path import isabs, isdir, isfile
from pathlib import Path
from shutil import move, rmtree, Error
from argparse import ArgumentParser, ArgumentError

from src.commands.history import cmd_history
from src.logger import logger
from src.errors import (
    path_doesnt_exist_message,
    missing_required_arguments_message,
    unknown_arguments_message,
    path_leads_to_dir_instead_of_file_message,
    path_leads_to_file_instead_of_dir_message,
    attempt_to_remove_parent_path_message,
)
from src.colortext import colorize


class Rm:
    "'rm' command to read file contents"

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
        """
        Execute 'rm' command from given directory with given args
        Args:
            cwd (str): directory to execute from
            _args (list[str]): args for 'rm' command
        """
        try:
            args, unknown_args = self.parser.parse_known_args(args=_args)
        except ArgumentError as e:
            missing_args = e.message[e.message.index(":") + 2 :]
            missing_required_arguments_message(missing_args_str=missing_args)
            return

        if len(unknown_args) > 0:
            unknown_arguments_message(unknown_args=unknown_args)

        path = str(
            Path(args.path if isabs(args.path) else f"{cwd}/{args.path}").resolve()
        )
        if not Path(path).exists():
            path_doesnt_exist_message(path=path)
            return

        # Decline command if it tries to delete root or parent directory
        if cwd and str(path) in cwd:
            attempt_to_remove_parent_path_message(path=path)
            return

        # Create .trash if it didn't exists
        if not Path("./.trash").exists():
            mkdir("./.trash")

        if args.recursive:
            if isfile(path):
                path_leads_to_file_instead_of_dir_message(path=path)
                return

            # Confirmation
            if not self.get_confirmation(path=path):
                logger.info("Action cancelled")
                return

            try:
                move(src=path, dst="./.trash")
            except Error:
                filename = path.split("\\")[-1]
                # Replace old file in .trash with new by deleting previous
                rmtree(f"./.trash/{filename}")
                move(src=path, dst="./.trash")
            if cwd:
                cmd_history.write(cmd=f"rm {path} --recursive")
        else:
            if isdir(path):
                path_leads_to_dir_instead_of_file_message(path=path)
                return

            try:
                move(src=path, dst="./.trash")
            except Error:
                filename = path.split("\\")[-1]
                # Replace old file in .trash with new by deleting previous
                remove(f"./.trash/{filename}")
                move(src=path, dst="./.trash")
            if cwd:
                cmd_history.write(cmd=f"rm {path}")

    def get_confirmation(self, path: str) -> bool:
        """
        Get confirmation from user to delete selected folder
        Args:
            path (str): path to folder
        Returns:
            bool: is deletion confirmed
        """
        msg1 = colorize(text="(y / n) Confirm folder deletion -", color="yellow")
        msg2 = colorize(text=path, color="yellow", bold=True)
        choice = input(f"{msg1} {msg2}\n")

        return choice == "y"


def clear_trash() -> None:
    "Delete .trash directory with all includes"
    if Path("./.trash").exists():
        rmtree("./.trash")


cmd_rm = Rm()
