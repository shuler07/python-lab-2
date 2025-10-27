from pathlib import Path

from src.constants import ANSI_COLOR_CODES


def colorize(text: str | Path, color: str, bold: bool = False) -> str:
    """
    Colorize given string
    Args:
        text (str | Path): string to be colorized
        color (str): string color (black, red, green, yellow, blue, magenta, lightblue, white)
        bold (bool): is string bold
    Returns:
        str: colorized string via ansi color codes
    """
    return f"\033[{1 if bold else 0};{ANSI_COLOR_CODES[color]}{text}\033[0m"
