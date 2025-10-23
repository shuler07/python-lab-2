from typing import Any
from os import system as sys, getcwd
import shlex

from src.commands.ls import Ls
from src.commands.cd import Cd
from src.commands.cat import Cat
from src.commands.cp import Cp
from src.commands.mv import Mv
from src.commands.rm import Rm
from src.commands.zip import Zip
from src.commands.unzip import Unzip
from src.commands.tar import Tar
from src.commands.untar import Untar
from src.commands.grep import Grep
from src.commands.history import History
from src.commands.undo import Undo

from src.logger import logger
from src.colortext import colorize


class Terminal3000:

    def __init__(self) -> None:
        self.cwd = getcwd()
        self.commands: dict[str, Any] = {
            "ls": Ls(),
            "cd": Cd(),
            "cat": Cat(),
            "cp": Cp(),
            "mv": Mv(),
            "rm": Rm(),
            "zip": Zip(),
            "unzip": Unzip(),
            "tar": Tar(),
            "untar": Untar(),
            "grep": Grep(),
            "history": History(),
            "undo": Undo(),
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
                | "tag"
                | "untar"
                | "grep"
            ):
                self.commands[cmd[0]].execute(cwd=self.cwd, _args=cmd[1:])
                self.commands["history"].write(cmd=command)
            case "cd":
                self.cwd = self.commands["cd"].execute(cwd=self.cwd, _args=cmd[1:])  # type: ignore
                self.commands["history"].write(cmd=command)
            case "history":
                self.commands["history"].execute(_args=cmd[1:])
            case "undo":
                self.commands["undo"].execute(
                    mark_undone_cmd=self.commands["history"].mark_undone  # type: ignore
                )
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
