from typing import Callable
from os import access, F_OK
from argparse import ArgumentParser

from src.errors import history_file_not_found_message, command_to_undo_not_found_message


class Undo:

    def __init__(self) -> None:
        parser = ArgumentParser(
            prog="undo",
            description="Undo last executed cp, mv or rm command",
            exit_on_error=False,
        )
        self.parser = parser

    def execute(self, mark_undone_cmd: Callable[[int], None]) -> None:
        if not access(path="./.history", mode=F_OK):
            history_file_not_found_message()
            return

        commands = open("./.history").readlines()[::-1]
        for cmd in commands:
            num, command, *args = cmd.split()

            if args and args[-1] == "(undone)":
                continue

            match command:
                case "cp":
                    mark_undone_cmd(int(num.rstrip(".")))
                    return
                case "mv":
                    mark_undone_cmd(int(num.rstrip(".")))
                    return
                case "rm":
                    mark_undone_cmd(int(num.rstrip(".")))
                    return
                case _:
                    continue

        command_to_undo_not_found_message()
