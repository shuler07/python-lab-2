from src.logger import logger
from src.colortext import colorize


def path_doesnt_exist_message(path: str) -> None:
    logger.warning('Path "%s" doesn\'t exist', path)

    msg1 = colorize(text="Path", color="red")
    msg2 = colorize(text=path, color="red", bold=True)
    msg3 = colorize(text="doesn't exist", color="red")
    print(msg1, msg2, msg3, sep=" ")


def unknown_arguments_message(unknown_args: list[str]) -> None:
    logger.warning("Unknown args: %s", ", ".join(unknown_args))

    msg1 = colorize(text="Unknown args:", color="yellow")
    msg2 = colorize(text=", ".join(unknown_args), color="yellow", bold=True)
    print(msg1, msg2, sep=" ")


def missing_required_arguments_message(missing_args_str: str) -> None:
    logger.error("Missing required arguments: %s", missing_args_str)

    msg1 = colorize(text="Missing required arguments:", color="red")
    msg2 = colorize(text=missing_args_str, color="red", bold=True)
    print(msg1, msg2, sep=" ")


def path_leads_to_dir_instead_of_file_message(path: str) -> None:
    logger.error('Directory path received instead of file path: "%s"', path)
    msg1 = colorize(text="Directory path received instead of file path:", color="red")
    msg2 = colorize(text=path, color="red", bold=True)
    print(msg1, msg2, sep=" ")


def path_leads_to_file_instead_of_dir_message(path: str) -> None:
    logger.error('File path received instead of directory path: "%s"', path)
    msg1 = colorize(text="File path received instead of directory path:", color="red")
    msg2 = colorize(text=path, color="red", bold=True)
    print(msg1, msg2, sep=" ")
