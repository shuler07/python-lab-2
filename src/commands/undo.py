from argparse import ArgumentParser
from src.commands.mv import cmd_mv
from src.commands.rm import cmd_rm
from src.commands.history import cmd_history
from src.errors import history_file_not_found_message


class Undo:
    "'undo' command to read file contents"

    def __init__(self) -> None:
        parser = ArgumentParser(
            prog="undo",
            description="Undo last executed cp, mv or rm command",
            exit_on_error=False,
        )
        self.parser = parser

    def execute(self) -> None:
        """
        Execute 'undo' command from given directory with given args
        Args:
            cwd (str): directory to execute from
            _args (list[str]): args for 'undo' command
        """
        from src import Path
        from src.errors import command_to_undo_not_found_message

        if not Path("./.history").exists():
            history_file_not_found_message()
            return

        # Check is history was initiated in current session
        if not cmd_history.initiated:
            command_to_undo_not_found_message()
            return

        # Search command to undo from end to begin
        commands = open("./.history").readlines()[::-1]
        line = len(commands) - 1

        for cmd in commands:
            # Check is commands in current session ended up
            if cmd.startswith("New session"):
                break

            _, command, *args = cmd.split()

            # Skip if command already undone
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
                        # Getting start index of filename in path
                        ind = args[-2].rfind("\\") + 1
                        _args = [
                            f"./.trash/{args[-2][ind:]}",
                            args[-2][:ind],
                        ]
                    else:
                        # Getting correct name of file in .trash
                        ind = args[-1].rfind("\\") + 1
                        _args = [
                            f"./.trash/{args[-1][ind:]}",
                            args[-1][:ind],
                        ]

                    cmd_mv.execute(cwd=None, _args=_args)
                    cmd_history.mark_undone(line=line)
                    return
                case _:
                    line -= 1
                    continue

        command_to_undo_not_found_message()


cmd_undo = Undo()
