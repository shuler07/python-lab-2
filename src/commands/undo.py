from os import access, F_OK
from argparse import ArgumentParser

from src.commands.rm import cmd_rm
from src.commands.history import cmd_history
from src.errors import history_file_not_found_message, command_to_undo_not_found_message


class Undo:

    def __init__(self) -> None:
        parser = ArgumentParser(
            prog="undo",
            description="Undo last executed cp, mv or rm command",
            exit_on_error=False,
        )
        self.parser = parser

    def execute(self) -> None:
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
                    _args = [args[-1]]
                    if args[-1] == "--recursive":
                        _args.append(args[-2])

                    cmd_rm.execute(cwd=None, _args=_args)
                    cmd_history.mark_undone(int(num.strip("()")))
                    return
                case "mv":
                    cmd_history.mark_undone(int(num.strip("()")))
                    return
                case "rm":
                    cmd_history.mark_undone(int(num.strip("()")))
                    return
                case _:
                    continue

        command_to_undo_not_found_message()


cmd_undo = Undo()
