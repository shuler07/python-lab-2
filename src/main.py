from typing import Any
from os import system as sys, getcwd
import shlex

from src.commands.ls import cmd_ls
from src.commands.cd import cmd_cd
from src.commands.cat import cmd_cat
from src.commands.cp import cmd_cp
from src.commands.mv import cmd_mv
from src.commands.rm import cmd_rm
from src.commands.zip import cmd_zip
from src.commands.unzip import cmd_unzip
from src.commands.tar import cmd_tar
from src.commands.untar import cmd_untar
from src.commands.grep import cmd_grep
from src.commands.history import cmd_history
from src.commands.undo import cmd_undo

from src.logger import logger
from src.colortext import colorize


class Terminal3000:

    def __init__(self) -> None:
        self.cwd = getcwd()
        self.commands: dict[str, Any] = {
            "ls": cmd_ls,
            "cd": cmd_cd,
            "cat": cmd_cat,
            "cp": cmd_cp,
            "mv": cmd_mv,
            "rm": cmd_rm,
            "zip": cmd_zip,
            "unzip": cmd_unzip,
            "tar": cmd_tar,
            "untar": cmd_untar,
            "grep": cmd_grep,
            "history": cmd_history,
            "undo": cmd_undo,
        }

        descriptions = [
            f"{cmd} - {self.commands[cmd].parser.description}"
            for cmd in self.commands.keys()
        ]
        self.help_message = f"""
This is Terminal3000 - very powerful tool for you
Available commands:
    {'\n    '.join(descriptions)}
    help - Show this help message
    cls - Clean screen
    quit - Quit Terminal3000 :(
"""

    def start(self) -> None:
        sys("cls")
        self.await_command()

    def await_command(self) -> None:
        msg1 = colorize(text="[T3000]", color="green", bold=True)
        msg2 = colorize(text=f"{self.cwd} 😊", color="green")
        command = input(f"{msg1} {msg2} \033[0;30m")

        logger.info("Received: %s", command)

        print("\033[0m", end="")
        self.process_command(command=command)

    def process_command(self, command: str) -> None:
        cmd = shlex.split(command.replace("\\", "/"))

        match cmd[0]:
            case (
                "ls"
                | "cat"
                | "cp"
                | "mv"
                | "rm"
                | "zip"
                | "unzip"
                | "tar"
                | "untar"
                | "grep"
            ):
                self.commands[cmd[0]].execute(cwd=self.cwd, _args=cmd[1:])
            case "cd":
                self.cwd = self.commands["cd"].execute(cwd=self.cwd, _args=cmd[1:])
            case "history":
                self.commands["history"].execute(_args=cmd[1:])
            case "undo":
                self.commands["undo"].execute()
            case "help":
                print(self.help_message)
            case "cls":
                sys("cls")
            case "quit":
                return
            case _:
                logger.error(
                    'The term "%s" is not recognised as the name of a command', cmd[0]
                )
                msg1 = colorize(text=cmd[0], color="red", bold=True)
                msg2 = colorize(
                    text="is not recognised as the name of a command", color="red"
                )
                print(f"{msg1} {msg2}")

        self.await_command()


def main() -> None:
    terminal = Terminal3000()
    terminal.start()


if __name__ == "__main__":
    main()
