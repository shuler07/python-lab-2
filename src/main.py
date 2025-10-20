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

from src.logger import logger
from src.colortext import colorize


class Terminal3000:

    def __init__(self) -> None:
        self.cwd = getcwd()
        self.commands: dict[
            str, Ls | Cd | Cat | Cp | Mv | Rm | Zip | Unzip | Tar | Untar
        ] = {
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
        }

        self.help_message = f"""
This is Terminal3000 - very powerful tool for you
Available commands:
    ls - {self.commands['ls'].parser.description}
    cd - {self.commands['cd'].parser.description}
    cat - {self.commands['cat'].parser.description}
    cp - {self.commands['cp'].parser.description}
    mv - {self.commands['mv'].parser.description}
    rm - {self.commands['rm'].parser.description}
    zip - {self.commands['zip'].parser.description}
    unzip - {self.commands['unzip'].parser.description}
    tar - {self.commands['tar'].parser.description}
    untar - {self.commands['untar'].parser.description}
    help - Show this help message
    cls - Clean screen
    quit - Quit Terminal3000 :(
"""

    def start(self) -> None:
        sys("cls")
        self.await_command()

    def await_command(self) -> None:
        msg1 = colorize(text="[T3000]", color="green", bold=True)
        msg2 = colorize(text=f"{self.cwd} #", color="green")
        command = input(f"{msg1} {msg2} \033[0;30m")
        logger.info("Received: %s", command)

        print("\033[0m", end="")
        self.process_command(command=command)

    def process_command(self, command: str) -> None:
        cmd = shlex.split(command.replace('\\', '/'))

        match cmd[0]:
            case "ls":
                self.commands["ls"].execute(cwd=self.cwd, _args=cmd[1:])
            case "cd":
                self.cwd = self.commands["cd"].execute(cwd=self.cwd, _args=cmd[1:])  # type: ignore
            case "cat":
                self.commands["cat"].execute(cwd=self.cwd, _args=cmd[1:])
            case "cp":
                self.commands["cp"].execute(cwd=self.cwd, _args=cmd[1:])
            case "mv":
                self.commands["mv"].execute(cwd=self.cwd, _args=cmd[1:])
            case "rm":
                self.commands["rm"].execute(cwd=self.cwd, _args=cmd[1:])
            case "zip":
                self.commands["zip"].execute(cwd=self.cwd, _args=cmd[1:])
            case "unzip":
                self.commands["unzip"].execute(cwd=self.cwd, _args=cmd[1:])
            case "tar":
                self.commands["tar"].execute(cwd=self.cwd, _args=cmd[1:])
            case "untar":
                self.commands["untar"].execute(cwd=self.cwd, _args=cmd[1:])
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
