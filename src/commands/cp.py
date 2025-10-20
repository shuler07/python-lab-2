from shutil import copy, copytree, SameFileError
from os import access, F_OK
from os.path import isabs, isfile
from argparse import ArgumentParser, ArgumentError

from src.errors import (
    path_doesnt_exist_message,
    unknown_arguments_message,
    missing_required_arguments_message,
    path_leads_to_file_instead_of_dir_message,
    permission_denied_message,
    src_and_dst_are_the_same_message,
)


class Cp:

    def __init__(self) -> None:
        parser = ArgumentParser(
            prog="cp",
            description="Copy file or folder from source to destination",
            exit_on_error=False,
        )
        parser.add_argument("src", help="Source of file or folder to copy from")
        parser.add_argument("dst", help="Destination of file or folder to copy where")
        parser.add_argument(
            "-r",
            "--recursive",
            action="store_true",
            help="Src folders only. Recursive copy of folders and files inside source folder",
        )
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

        srcpath = args.src if isabs(args.src) else f"{cwd}\{args.src}"
        dstpath = args.dst if isabs(args.dst) else f"{cwd}\{args.dst}"
        if not access(path=srcpath, mode=F_OK):
            path_doesnt_exist_message(path=srcpath)
            return

        if args.recursive:
            if isfile(srcpath):
                path_leads_to_file_instead_of_dir_message(path=srcpath)
                return

            try:
                copytree(src=srcpath, dst=dstpath, dirs_exist_ok=True)
            except PermissionError:
                permission_denied_message(srcpath, dstpath)
        else:
            try:
                copy(src=srcpath, dst=dstpath)
            except PermissionError:
                permission_denied_message(srcpath, dstpath)
            except SameFileError:
                src_and_dst_are_the_same_message(path=srcpath)
