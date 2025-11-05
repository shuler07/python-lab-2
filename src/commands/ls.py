from datetime import datetime as dt
from argparse import ArgumentParser
from src.commands.history import cmd_history
from src.errors import (
    path_doesnt_exist_message,
    unknown_arguments_message,
    path_leads_to_file_instead_of_dir_message,
)
from src.colortext import colorize
from src.constants import (
    DATETIME_FORMAT,
    LS_FILE_SIZE_COLUMN_WIDTH,
    LS_DATETIME_COLUMN_WIDTH,
    LS_PERMS_COLUMN_WIDTH,
)


class Ls:
    "'ls' command to read file contents"

    def __init__(self) -> None:
        parser = ArgumentParser(
            prog="ls",
            description="Show files and folders in current or specified folder",
            exit_on_error=False,
        )
        parser.add_argument("path", help='Directory path (default = ".")', nargs="?")
        parser.add_argument(
            "-l",
            "--list",
            action="store_true",
            help="Show more information about files",
        )
        self.parser = parser

    def execute(self, cwd: str, _args: list[str]) -> None:
        """
        Execute 'ls' command from given directory with given args
        Args:
            cwd (str): directory to execute from
            _args (list[str]): args for 'ls' command
        """
        from src import listdir, access, R_OK, W_OK, isfile, isabs, getsize, getctime, getmtime, Path

        args, unknown_args = self.parser.parse_known_args(args=_args)
        if len(unknown_args) > 0:
            unknown_arguments_message(unknown_args=unknown_args)

        #  Default path of directory to be listed
        args.path = args.path if args.path else "."

        path = str(
            Path(args.path if isabs(args.path) else f"{cwd}/{args.path}").resolve()
        )
        if not Path(path).exists():
            path_doesnt_exist_message(path=path)
            return
        if isfile(path):
            path_leads_to_file_instead_of_dir_message(path=path)
            return

        if args.list:
            #  For File name column correct width
            max_len_elem = max(max(len(x) for x in listdir(path=path)), 9)

            #  Head of table
            head = colorize(
                text=f"{'File name': ^{max_len_elem}}  {'File size': ^{LS_FILE_SIZE_COLUMN_WIDTH}}  {'File created': ^{LS_DATETIME_COLUMN_WIDTH}}  {'File modified': ^{LS_DATETIME_COLUMN_WIDTH}}  {'Permissions': ^{LS_PERMS_COLUMN_WIDTH}}",
                color="white",
                bold=True,
            )
            print(head)

            def el_name(x: str) -> str:
                return f"{x: <{max_len_elem}}"

            def el_size(x: str) -> str:
                return f"{getsize(f'{path}/{x}'): <{LS_FILE_SIZE_COLUMN_WIDTH}}"

            def el_created(x: str) -> str:
                return f"{str(dt.fromtimestamp(getctime(f'{path}/{x}')).strftime(DATETIME_FORMAT)): <{LS_DATETIME_COLUMN_WIDTH}}"

            def el_modified(x: str) -> str:
                return f"{str(dt.fromtimestamp(getmtime(f'{path}/{x}')).strftime(DATETIME_FORMAT)): <{LS_DATETIME_COLUMN_WIDTH}}"

            def el_access(x: str) -> str:
                perms = []
                if access(f"{path}/{x}", R_OK):
                    perms.append("Read")
                if access(f"{path}/{x}", W_OK):
                    perms.append("Write")
                return f"{', '.join(perms): <{LS_PERMS_COLUMN_WIDTH}}"

            #  Files and dirs with its data
            for el in listdir(path=path):
                print(
                    "  ".join(
                        [
                            el_name(el),
                            el_size(el),
                            el_created(el),
                            el_modified(el),
                            el_access(el),
                        ]
                    )
                )

            cmd_history.write(cmd=f"ls {path} --list")
        else:
            [print(elem) for elem in listdir(path=path)]
            cmd_history.write(cmd=f"ls {path}")


cmd_ls = Ls()
