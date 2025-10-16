from src.argparser import ArgParser
from src.colortext import colorize
from src.constants import LS_COMMAND_FILE_SIZE_COLUMN_WIDTH

from os import system as sys
from os import listdir
from os.path import getsize


class SuperTerminal3000:

    def __init__(self, debug: bool = False) -> None:
        self.parser = ArgParser()
        self.help_message = f"""
This is SuperTerminal3000 - very powerful tool for you
Available commands:
    ls - {self.parser.lsParser.description}
    cd - {self.parser.cdParser.description}
"""

    def start(self) -> None:
        sys("cls")
        self.await_command()

    def await_command(self) -> None:
        msg1 = colorize(text="[super-terminal-3000]", color="green", bold=True)
        msg2 = colorize(text="#", color="green")
        command = input(f"{msg1} {msg2} \033[0;30m")

        print("\033[0m", end="")
        self.process_command(command=command)

    def process_command(self, command: str) -> None:
        cmd = command.split()

        match cmd[0]:
            case "ls":
                args = self.parser.parse(cmd="ls", args=cmd[1:])
                self.ls(args.path, args.list)
            case "cd":
                pass
            case "help":
                print(self.help_message)
            case _:
                msg1 = colorize(text=cmd[0], color="red", bold=True)
                msg2 = colorize(
                    text="is not recognised as the name of a command", color="red"
                )
                print(f"{msg1} {msg2}")

        self.await_command()

    def ls(self, path: str, list: str | None):
        if list:
            max_len_elem = max(max(len(x) for x in listdir(path=path)), 9)
            head = colorize(
                text=f"{'File name': ^{max_len_elem}}  {'File size': ^{LS_COMMAND_FILE_SIZE_COLUMN_WIDTH}}",
                color="white",
                bold=True,
            )
            print(head)

            for elem in listdir(path=path):
                print(
                    f"{elem: <{max_len_elem}}  {getsize(f'{path}/{elem}'): <{LS_COMMAND_FILE_SIZE_COLUMN_WIDTH}}"
                )
        else:
            [print(elem) for elem in listdir(path=path)]


def main() -> None:
    terminal = SuperTerminal3000(debug=True)
    terminal.start()


if __name__ == "__main__":
    main()
