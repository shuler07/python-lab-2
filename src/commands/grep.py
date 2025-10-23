from os import access, F_OK, listdir, walk
from os.path import isabs, isfile, join
from argparse import ArgumentParser, ArgumentError
import re

from src.errors import (
    path_doesnt_exist_message,
    missing_required_arguments_message,
    unknown_arguments_message,
    path_leads_to_file_instead_of_dir_message,
    unsupported_file_format_message,
)
from src.colortext import colorize


class Grep:

    def __init__(self) -> None:
        parser = ArgumentParser(
            prog="grep",
            description="Find files with text satisfying given pattern",
            exit_on_error=False,
        )
        parser.add_argument("pattern", help="Pattern of text to search")
        parser.add_argument("path", help="Path to folder or file where to search")
        parser.add_argument(
            "-r",
            "--recursive",
            action="store_true",
            help="Recursive search in subfolders",
        )
        parser.add_argument(
            "-i", "--insensetive", action="store_true", help="Search case insensetive"
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

        path = args.path if isabs(args.path) else f"{cwd}\{args.path}"
        if not access(path=path, mode=F_OK):
            path_doesnt_exist_message(path=path)
            return

        if args.recursive:
            if isfile(path):
                path_leads_to_file_instead_of_dir_message(path=path)
                return

            for root, _, files in walk(path):
                for file in files:
                    filepath = join(root, file)
                    self.search_pattern(
                        path=filepath,
                        pattern=args.pattern,
                        insensetive=args.insensetive,
                    )
        else:
            if isfile(path):
                self.search_pattern(
                    path=path, pattern=args.pattern, insensetive=args.insensetive
                )
            else:
                for file in listdir(path=path):
                    filepath = join(path, file)
                    if isfile(path=filepath):
                        self.search_pattern(
                            path=filepath,
                            pattern=args.pattern,
                            insensetive=args.insensetive,
                        )

    def search_pattern(self, path: str, pattern: str, insensetive: bool) -> None:
        flag = re.IGNORECASE if insensetive else 0
        pattern = rf"{pattern}"
        found = []

        try:
            for n, line in enumerate(open(file=path).readlines(), start=1):
                for i in re.finditer(pattern=pattern, string=line, flags=flag):
                    found.append(f'Line {n}: "{i.group()}" at position {i.span()[0]}')
        except UnicodeDecodeError:
            unsupported_file_format_message(path=path)
            return

        if len(found) > 0:
            print(colorize(text=f"File: {path}", color="blue"), "\033[0m")
            for f in found:
                print(f)
