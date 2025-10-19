from os import access, F_OK
from os.path import isabs
from shutil import move, Error as PathAlreadyExistsError, copytree, rmtree
from argparse import ArgumentParser, ArgumentError

from src.errors import (
    path_doesnt_exist_message,
    missing_required_arguments_message,
    unknown_arguments_message,
    permission_denied_message,
    clear_path,
    src_and_dst_are_the_same_message,
)


class Mv:

    def __init__(self) -> None:
        parser = ArgumentParser(
            prog="mv",
            description="Move file or folder from source to destination, rename file or folder",
        )
        parser.add_argument(
            "src", help="Source of file or folder to move from or rename"
        )
        parser.add_argument(
            "dst", help="Destination of file or folder to move where or new name"
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

        try:
            move(src=srcpath, dst=dstpath)
        except PermissionError:
            permission_denied_message(srcpath, dstpath)
        except PathAlreadyExistsError:
            real_src_path = clear_path(srcpath)[: clear_path(srcpath).rindex("\\")]
            real_dst_path = clear_path(dstpath).rstrip("\\")
            if real_src_path == real_dst_path:
                src_and_dst_are_the_same_message(path=srcpath)
                return

            copytree(
                src=srcpath,
                dst=f'{dstpath}\{srcpath.split('\\')[-1]}',
                dirs_exist_ok=True,
            )
            rmtree(path=srcpath)
