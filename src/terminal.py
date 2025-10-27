from typing import Any
from os import system as sys, getcwd
import shlex

from src.commands.ls import cmd_ls
from src.commands.cd import cmd_cd
from src.commands.cat import cmd_cat
from src.commands.cp import cmd_cp
from src.commands.mv import cmd_mv
from src.commands.rm import cmd_rm, clear_trash
from src.commands.zip import cmd_zip
from src.commands.unzip import cmd_unzip
from src.commands.tar import cmd_tar
from src.commands.untar import cmd_untar
from src.commands.grep import cmd_grep
from src.commands.history import cmd_history
from src.commands.undo import cmd_undo

from src.errors import term_is_not_recognised_message
from src.logger import logger
from src.colortext import colorize


class Terminal3000:
    """
    Very powerful terminal with bunch of useful commands
    """

    def __init__(self, cwd: str = getcwd(), reload: bool = True) -> None:
        self.cwd = cwd
        self.reload = reload
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
            f"\033[1;37m{cmd}\033[0m - {self.commands[cmd].parser.description}"
            for cmd in self.commands.keys()
        ]
        self.help_message = f"""
\033[1;35mThis is Terminal3000 - very powerful tool for you 💪\033[0m
\033[1;36mAvailable commands:\033[0m
    {'\n    '.join(descriptions)}
    \033[1;37mh, help\033[0m - Show this help message
    \033[1;37mcls, clear\033[0m - Clean screen
    \033[1;37mq, quit\033[0m - Quit Terminal3000 :(
"""

    def start(self) -> None:
        "Start terminal session"
        sys("cls")
        self.wait()

    def wait(self) -> None:
        "Wait command from user"
        msg1 = colorize(text="[T-3000]", color="green", bold=True)
        msg2 = colorize(text=self.cwd, color="green")

        command = input(f"{msg1} {msg2} \033[0;30m")
        print("\033[0m", end="")

        logger.info("Received: %s", command)

        self.process(command=command)

    def process(self, command: str) -> None:
        """
        Process given command
        Args:
            command (str): command to be proccessed
        """
        # Split command taking into account arguments in quotes
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
            case "h" | "help":
                print(self.help_message)
            case "cls" | "clear":
                sys("cls")
            case "q" | "quit":
                clear_trash()
                return
            case _:
                term_is_not_recognised_message(cmd=cmd[0])

        if self.reload:
            self.wait()
