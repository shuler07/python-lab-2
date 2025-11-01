from shutil import SameFileError, Error as PathAlreadyExistsError
from argparse import ArgumentParser, ArgumentError
from src.commands.history import cmd_history
from src.errors import (
    path_doesnt_exist_message,
    unknown_arguments_message,
    missing_required_arguments_message,
    path_leads_to_file_instead_of_dir_message,
    path_leads_to_dir_instead_of_file_message,
    permission_denied_message,
    src_and_dst_are_the_same_message,
)


class Cp:
    "'cp' command to read file contents"

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
        """
        Execute 'cp' command from given directory with given args
        Args:
            cwd (str): directory to execute from
            _args (list[str]): args for 'cp' command
        """
        from src import isabs, isdir, isfile, copy, copytree, Path

        try:
            args, unknown_args = self.parser.parse_known_args(args=_args)
        except ArgumentError as e:
            missing_args = e.message[e.message.index(":") + 2 :]
            missing_required_arguments_message(missing_args_str=missing_args)
            return

        if len(unknown_args) > 0:
            unknown_arguments_message(unknown_args=unknown_args)

        srcpath = str(
            Path(args.src if isabs(args.src) else f"{cwd}/{args.src}").resolve()
        )
        dstpath = str(
            Path(args.dst if isabs(args.dst) else f"{cwd}/{args.dst}").resolve()
        )
        if not Path(srcpath).exists():
            path_doesnt_exist_message(path=srcpath)
            return

        if args.recursive:
            if isfile(srcpath):
                path_leads_to_file_instead_of_dir_message(path=srcpath)
                return

            foldername = srcpath.split("\\")[-1]
            dstpath = f"{dstpath}/{foldername}"
            try:
                cmd_history.write(
                    cmd=f"cp {srcpath} {copytree(src=srcpath, dst=dstpath, dirs_exist_ok=True)} --recursive"
                )
            except PermissionError:
                permission_denied_message(srcpath, dstpath)
            except PathAlreadyExistsError:
                src_and_dst_are_the_same_message(path=srcpath)
        else:
            if isdir(srcpath):
                path_leads_to_dir_instead_of_file_message(path=srcpath)
                return

            try:
                cmd_history.write(cmd=f"cp {srcpath} {copy(src=srcpath, dst=dstpath)}")
            except PermissionError:
                permission_denied_message(srcpath, dstpath)
            except SameFileError:
                src_and_dst_are_the_same_message(path=srcpath)


cmd_cp = Cp()
