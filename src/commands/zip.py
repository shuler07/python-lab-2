from os import walk
from os.path import isabs, isfile, join
from pathlib import Path
from zipfile import ZipFile
from argparse import ArgumentParser, ArgumentError

from src.commands.history import cmd_history
from src.errors import (
    path_doesnt_exist_message,
    missing_required_arguments_message,
    unknown_arguments_message,
    path_leads_to_file_instead_of_dir_message,
)


class Zip:
    "'zip' command to read file contents"

    def __init__(self):
        parser = ArgumentParser(
            prog="zip",
            description="Create zip archive from folder",
            exit_on_error=False,
        )
        parser.add_argument("path", help="Path to folder to zip")
        parser.add_argument("name", help="Zip archive name", nargs="?")
        self.parser = parser

    def execute(self, cwd: str, _args: list[str]) -> None:
        """
        Execute 'zip' command from given directory with given args
        Args:
            cwd (str): directory to execute from
            _args (list[str]): args for 'zip' command
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
        if isfile(path):
            path_leads_to_file_instead_of_dir_message(path=path)
            return

        # Make valid name of archive
        zipname = args.name if args.name else f'{path.split('\\')[-1]}.zip'
        if not zipname.endswith(".zip"):
            zipname += ".zip"

        # Make valid path
        zippath = f"{cwd}/{zipname}"

        with ZipFile(file=zippath, mode="w") as zipw:
            ind_real_root_begin = None
            for root, _, files in walk(top=path):
                if ind_real_root_begin is None:
                    ind_real_root_begin = len(root.split("\\")) - 1

                real_root = join(*root.split("\\")[ind_real_root_begin:])
                for file in files:
                    filepath = join(root, file)
                    arcname = join(real_root, file)
                    zipw.write(filename=filepath, arcname=arcname)

        cmd_history.write(cmd=f"zip {path} {zipname}")


cmd_zip = Zip()
