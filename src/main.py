from os import system as sys, getcwd
from pathlib import Path

from src.commands.ls import Ls
from src.commands.cd import Cd
from src.commands.cat import Cat
from src.commands.cp import Cp
from src.logger import logger
from src.colortext import colorize


class Terminal3000:

    def __init__(self) -> None:
        self.cwd = getcwd()
        self.commands: dict[str, Ls | Cd | Cat | Cp] = {
            "ls": Ls(),
            "cd": Cd(),
            "cat": Cat(),
            "cp": Cp(),
        }

        self.help_message = f"""
This is Terminal3000 - very powerful tool for you
Available commands:
    ls - {self.commands['ls'].parser.description}
    cd - {self.commands['cd'].parser.description}
    cat - {self.commands['cat'].parser.description}
    cp - {self.commands['cp'].parser.description}
    help - Show this help message
    quit - Quit Terminal3000 :(
"""

    def start(self) -> None:
        sys("cls")
        self.await_command()

    def await_command(self) -> None:
        msg1 = colorize(text="[T3000]", color="green", bold=True)
        msg2 = colorize(text=f"{Path(self.cwd)} #", color="green")
        command = input(f"{msg1} {msg2} \033[0;30m")
        logger.info("Received: %s", command)

        print("\033[0m", end="")
        self.process_command(command=command)

    def process_command(self, command: str) -> None:
        cmd = command.split()

        match cmd[0]:
            case "ls":
                self.commands["ls"].execute(cwd=self.cwd, _args=cmd[1:])
            case "cd":
                self.cwd = self.commands["cd"].execute(cwd=self.cwd, _args=cmd[1:])  # type: ignore
            case "cat":
                self.commands["cat"].execute(cwd=self.cwd, _args=cmd[1:])
            case "cp":
                self.commands["cp"].execute(cwd=self.cwd, _args=cmd[1:])
            case "help":
                print(self.help_message)
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
