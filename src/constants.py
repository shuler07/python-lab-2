from pathlib import Path


DATETIME_FORMAT = "%Y/%m/%d %H:%M:%S"

LS_FILE_SIZE_COLUMN_WIDTH = 14
LS_DATETIME_COLUMN_WIDTH = 20
LS_PERMS_COLUMN_WIDTH = 12

TESTS_DIR = f"{Path().cwd()}\\tests\\folder_for_tests"

ANSI_COLOR_CODES = {
    "black": "30m",
    "red": "31m",
    "green": "32m",
    "yellow": "33m",
    "blue": "34m",
    "magenta": "35m",
    "lightblue": "36m",
    "white": "37m",
}
