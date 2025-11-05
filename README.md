# (Rus) Лабораторная работа #2
Невероятно функциональный, красивый и незаменимый Terminal3000 — это терминал нового поколения, рядом с которым и рядом не стояли PowerShell и Bash.

## Реализованный функционал
1. ls [-h, --help] [-l, --list] [path] — Показать файлы и папки в текущей или указанной папке
2. cd [-h, --help] path — Сменить текущий каталог
3. cat [-h, --help] path — Прочитать содержимое файла
4. cp [-h, --help] [-r, --recursive] src dst — Копировать файл или папку из исходной папки в целевую
5. mv [-h, --help] src dst — Переместить файл или папку из исходной папки в целевую, переименовать файл или папку
6. rm [-h, --help] [-r, --recursive] path — Удалить файл или папку
7. zip [-h, --help] path name — Создать zip-архив из папки
8. unzip [-h, --help] path name — Распаковать архив в папку
9. tar [-h, --help] path name — Создать tar-архив из папка
10. untar [-h, --help] oath — распаковать архив в папку
11. grep [-h, --help] [-r, --recursive] [-i, --insensetive] path pattern — найти файлы с текстом, удовлетворяющим заданному шаблону
12. history [-h, --help] [-c, --count COUNT] — показать последние выполненные команды
13. undo — отменить последнюю выполненную команду
14. help — показать справку
15. cls, clear — очистить вывод терминала
16. quit — выйти из терминала

Также:
- Ведение журнала в t3000.log
- Временный каталог .trash для удалённых файлов и папок, который очищается после выхода из терминала
- Файл .history с данными о последних сеансах и выполненных командах

## Структура проекта

<pre>
    .
    ├── src/                               # Исходный код  
    │   ├─── commands/                     # Исходный код команд терминала
    │   │   ├─── ls.py                     # Класс команды ls
    │   │   ├─── cd.py                     # Класс команды cd
    │   │   ├─── cat.py                    # Класс команды cat
    │   │   ├─── cp.py                     # Класс команды cp
    │   │   ├─── mv.py                     # Класс команды mv
    │   │   ├─── rm.py                     # Класс команды rm
    │   │   ├─── zip.py                    # Класс команды zip
    │   │   ├─── unzip.py                  # Класс команды unzip
    │   │   ├─── tar.py                    # Класс команды tar
    │   │   ├─── untar.py                  # Класс команды untar
    │   │   ├─── grep.py                   # Класс команды grep
    │   │   ├─── history.py                # Класс команды history
    │   │   ├─── undo.py                   # Класс команды undo
    │   ├── colortext.py                   # Функция colorize для цветного текста
    │   ├── constants.py                   # Константы
    │   ├── errors.py                      # Сообщения об ошибках и их логирование
    │   ├── logger.py                      # Логгер
    │   ├── main.py                        # Точка входа
    │   ├── terminal.py                    # Класс терминала
    ├── tests/                             # Тесты
    │   ├── test_terminal.py               # Тест отработки терминала
    ├── uv.lock                            # Зависимости проекта
    ├── .gitignore                         # .gitignore файл
    ├──.pre-commit-config.yaml             # Средства автоматизации проверки кодстайла
    ├── README.md                          # Описание проекта, этот файл
</pre>

## Как использовать
1. Запустите терминал (python -m src.main)
2. Наслаждайтесь!

# (Eng) Lab #2
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

## Project Structure

<pre>
    .
    ├── src/                               # Source code
    │   ├─── commands/                     # Source code for terminal commands
    │   │   ├─── ls.py                     # Ls command class
    │   │   ├─── cd.py                     # Cd command class
    │   │   ├─── cat.py                    # Cat command class
    │   │   ├─── cp.py                     # Cp command class
    │   │   ├─── mv.py                     # Mv command class
    │   │   ├─── rm.py                     # Rm command class
    │   │   ├─── zip.py                    # Zip command class
    │   │   ├─── unzip.py                  # Unzip command class
    │   │   ├─── tar.py                    # Tar command class
    │   │   ├─── untar.py                  # Untar command class
    │   │   ├─── grep.py                   # Grep command class
    │   │   ├─── history.py                # History command class
    │   │   ├─── undo.py                   # Undo command class
    │   ├── colortext.py                   # Colorize function for colored text
    │   ├── constants.py                   # Constants
    │   ├── errors.py                      # Error messages and logging errors
    │   ├── logger.py                      # Logger
    │   ├── main.py                        # Entry point
    │   ├── terminal.py                    # Terminal class
    ├── tests/                             # Tests
    │   ├── test_terminal.py               # Test of terminal work
    ├── uv.lock                            # Project dependencies
    ├── .gitignore                         # .gitignore file
    ├──.pre-commit-config.yaml             # Codestyle verification automation tools
    ├── README.md                          # Project description, this file
</pre>

## How to use
1. Launch terminal (python -m src.main)
2. Enjoy it!
