from os import access, F_OK
from argparse import ArgumentParser

from src.commands.mv import cmd_mv
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

        if not cmd_history.initiated:
            command_to_undo_not_found_message()
            return

        commands = open("./.history").readlines()[::-1]
        line = len(commands) - 1
        for cmd in commands:
            if cmd.startswith("New session"):
                command_to_undo_not_found_message()
                return
            _, command, *args = cmd.split()

            if args and args[-1] == "(undone)":
                line -= 1
                continue

            match command:
                case "cp":
                    _args = [args[-1]]
                    if args[-1] == "--recursive":
                        _args.append(args[-2])

                    cmd_rm.execute(cwd=None, _args=_args)
                    cmd_history.mark_undone(line=line)
                    return
                case "mv":
                    _args = [args[-1], args[-2]]

                    cmd_mv.execute(cwd=None, _args=_args)
                    cmd_history.mark_undone(line=line)
                    return
                case "rm":
                    _args = []
                    if args[-1] == "--recursive":
                        _args = [
                            f'./.trash/{args[-2].split('\\')[-1]}',
                            args[-2][args[-2].rfind("\\") + 1 :],
                        ]
                    else:
                        _args = [
                            f'./.trash/{args[-1].split('\\')[-1]}',
                            args[-1][args[-1].rfind("\\") + 1 :],
                        ]

                    cmd_mv.execute(cwd=None, _args=_args)
                    cmd_history.mark_undone(line=line)
                    return
                case _:
                    line -= 1
                    continue

        command_to_undo_not_found_message()


cmd_undo = Undo()
