from src.logger import logger
from src.colortext import colorize


def term_is_not_recognised_message(cmd: str) -> None:
    logger.error('The term "%s" is not recognised as the name of a command', cmd)
    msg1 = colorize(text=cmd, color="red", bold=True)
    msg2 = colorize(text="is not recognised as the name of a command 😞", color="red")
    print(msg1, msg2, sep=" ")


def path_doesnt_exist_message(path: str) -> None:
    logger.warning('Path "%s" doesn\'t exist', path)

    msg1 = colorize(text="😞 Path", color="red")
    msg2 = colorize(text=path, color="red", bold=True)
    msg3 = colorize(text="doesn't exist", color="red")
    print(msg1, msg2, msg3, sep=" ")


def unknown_arguments_message(unknown_args: list[str]) -> None:
    logger.warning("Unknown args: %s", ", ".join(unknown_args))

    msg1 = colorize(text="🤔 Unknown args:", color="yellow")
    msg2 = colorize(text=", ".join(unknown_args), color="yellow", bold=True)
    print(msg1, msg2, sep=" ")


def missing_required_arguments_message(missing_args_str: str) -> None:
    logger.error("Missing required arguments: %s", missing_args_str)

    msg1 = colorize(text="😭 Missing required arguments:", color="red")
    msg2 = colorize(text=missing_args_str, color="red", bold=True)
    print(msg1, msg2, sep=" ")


def path_leads_to_dir_instead_of_file_message(path: str) -> None:
    logger.error('Directory path received instead of file path: "%s"', path)

    msg1 = colorize(
        text="😕 Directory path received instead of file path:", color="red"
    )
    msg2 = colorize(text=path, color="red", bold=True)
    print(msg1, msg2, sep=" ")


def path_leads_to_file_instead_of_dir_message(path: str) -> None:
    logger.error('File path received instead of directory path: "%s"', path)

    msg1 = colorize(
        text="😕 File path received instead of directory path:", color="red"
    )
    msg2 = colorize(text=path, color="red", bold=True)
    print(msg1, msg2, sep=" ")


def permission_denied_message(*paths: str) -> None:
    logger.error("Permission denied: %s", " or ".join(f'"{path}"' for path in paths))

    msg1 = colorize(text="😞 Permission denied:", color="red")
    msg2 = colorize(text=" or ".join(paths), color="red", bold=True)
    print(msg1, msg2, sep=" ")


def src_and_dst_are_the_same_message(path: str) -> None:
    logger.error('Source and destination are equal: "%s"', path)

    msg1 = colorize(text="😕 Source and destination are equal:", color="red")
    msg2 = colorize(text=path, color="red", bold=True)
    print(msg1, msg2, sep=" ")


def path_doesnt_lead_to_zipfile_message(path: str) -> None:
    logger.error('Path doesn\'t lead to zipfile: "%s"', path)

    msg1 = colorize(text="😕 Path doesn't lead to zipfile:", color="red")
    msg2 = colorize(text=path, color="red", bold=True)
    print(msg1, msg2, sep=" ")


def path_doesnt_lead_to_tarfile_message(path: str) -> None:
    logger.error('Path doesn\'t lead to tarfile: "%s"', path)

    msg1 = colorize(text="😕 Path doesn't lead to tarfile:", color="red")
    msg2 = colorize(text=path, color="red", bold=True)
    print(msg1, msg2, sep=" ")


def attempt_to_remove_parent_path_message(path: str) -> None:
    logger.error("Attempt to remove parent path: %s", path)

    msg1 = colorize(text="😡 Attempt to remove parent path:", color="red")
    msg2 = colorize(text=path, color="red", bold=True)
    print(msg1, msg2, sep=" ")


def unsupported_file_format_message(path: str) -> None:
    logger.error("Unsupported file format: %s", path)


def history_file_not_found_message() -> None:
    logger.error("History file not found")

    print(colorize(text="😞 History file not found", color="red"))


def command_to_undo_not_found_message() -> None:
    logger.error("Not found any command to undo")

    print(colorize(text="😞 Not found any command to undo", color="red"))
