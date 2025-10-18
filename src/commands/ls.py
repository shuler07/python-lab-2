from os import listdir, access, R_OK, W_OK
from os.path import getsize, getctime, getmtime
from datetime import datetime as dt
import argparse

from src.logger import logger
from src.colortext import colorize
from src.constants import (
    LS_FILE_SIZE_COLUMN_WIDTH,
    LS_DATETIME_COLUMN_WIDTH,
    LS_DATETIME_FORMAT,
    LS_PERMS_COLUMN_WIDTH,
)


class Ls:

    def __init__(self) -> None:
        parser = argparse.ArgumentParser(
            prog="ls",
            description="Show files and folders in current or specified folder",
            exit_on_error=False,
        )
        parser.add_argument("path", help="Set path", nargs="?")
        parser.add_argument(
            "-l",
            "--list",
            action="store_true",
            help="Show more information about files",
        )
        self.parser = parser

    def execute(self, cwd: str, _args: list[str]) -> None:
        args, unknown_args = self.parser.parse_known_args(args=_args)
        if len(unknown_args) > 0:
            logger.warning("Invalid args: %s", ", ".join(unknown_args))
        path = f"{cwd}/{args.path if args.path else '.'}"

        if args.list:
            max_len_elem = max(max(len(x) for x in listdir(path=path)), 9)

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
                return f"{str(dt.fromtimestamp(getctime(f'{path}/{x}')).strftime(LS_DATETIME_FORMAT)): <{LS_DATETIME_COLUMN_WIDTH}}"

            def el_modified(x: str) -> str:
                return f"{str(dt.fromtimestamp(getmtime(f'{path}/{x}')).strftime(LS_DATETIME_FORMAT)): <{LS_DATETIME_COLUMN_WIDTH}}"

            def el_access(x: str) -> str:
                perms = []
                if access(f"{path}/{x}", R_OK):
                    perms.append("Read")
                if access(f"{path}/{x}", W_OK):
                    perms.append("Write")
                return f"{', '.join(perms): <{LS_PERMS_COLUMN_WIDTH}}"

            for el in listdir(path=path):
                print(
                    f"{el_name(el)}  {el_size(el)}  {el_created(el)}  {el_modified(el)}  {el_access(el)}"
                )
        else:
            [print(elem) for elem in listdir(path=path)]
