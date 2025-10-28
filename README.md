# Lab #2
The incredibly functional awesome beautiful indispensable Terminal3000 is a next-generation terminal that leaves nothing to be desired, even compared to PowerShell and Bash.

## Implemented commands functionality
1. ls [-h, --help] [-l, --list] [path] - Show files and folders in current or specified folder
2. cd [-h, --help] path - Change current directory
3. cat [-h, --help] path - Read file contents
4. cp [-h, --help] [-r, --recursive] src dst - Copy file or folder from source to destination
5. mv [-h, --help] src dst - Move file or folder from source to destination, rename file or folder
6. rm [-h, --help] [-r, --recursive] path - Remove file or folder
7. zip [-h, --help] path name - Create zip archive from folder
8. unzip [-h, --help] path - Unzip archive to folder
9. tar [-h, --help] path name - Create tar archive from folder
10. untar [-h, --help] path - Untar archive to folder
11. grep [-h, --help] [-r, --recursive] [-i, --insensetive] pattern path - Find files with text satisfying given pattern
12. history [-h, --help] [-c, --count COUNT] - Show last executed commands
13. undo - Undo last executed command
14. help - Show help message
15. cls, clear - Clean terminal output
16. quit - Quit terminal

Also:
- Logging in t3000.log
- Temporary .trash directory for removed files and folders, that clears after quitting terminal
- .history file with data about last sessions and executed commands

## How to user
1. Launch terminal (python -m src.main)
2. Enjoy it!
   Например: 2 + $$3 - ~~2 некорректное выражение
3. Не допускается использование сокращенной записи умножения без знака.
   Например: 2 * (3 * 2) корректное выражение
             2(3 * 2) некорректное выражение
4. Допускается возведение степени в степень без использования скобок.
   Например: 2 ** ~2 ** ~2 корректное выражение (трактуется как 2 ** (~2 ** (~2)))
