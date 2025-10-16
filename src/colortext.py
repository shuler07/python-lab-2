ansi_color_codes = {
    "black": "30m",
    "red": "31m",
    "green": "32m",
    "yellow": "33m",
    "blue": "34m",
    "magenta": "35m",
    "lightblue": "36m",
    "white": "37m",
}


def colorize(text: str, color: str, bold: bool = False) -> str:
    return f"\033[{1 if bold else 0};{ansi_color_codes[color]}{text}\033[0m"
