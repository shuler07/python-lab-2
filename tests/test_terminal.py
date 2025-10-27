from os import access, F_OK
from pathlib import Path

from src.terminal import Terminal3000
from src.constants import TESTS_DIR

terminal = Terminal3000(cwd=TESTS_DIR, reload=False)


class TestTerminal3000:

    # ls
    def test_ls_1(self, capsys):
        terminal.process("ls")

        captured = capsys.readouterr()
        expected = "somefile1.txt\nsomefile2.txt\nsubfolder_for_tests\n"
        assert captured.out == expected

    def test_ls_2(self, capsys):
        terminal.process("ls ././..\\folder_for_tests/subfolder_for_tests\\./")

        captured = capsys.readouterr()
        expected = "somefile3.txt\n"
        assert captured.out == expected

    def test_ls_3(self, capsys):
        terminal.process("ls subfolder_for_tests -kklkkjgkklhjgkg")

        captured = capsys.readouterr()
        expected = "\033[0;33m🤔 Unknown args:\033[0m \033[1;33m-kklkkjgkklhjgkg\033[0m\nsomefile3.txt\n"
        assert captured.out == expected

    # cd
    def test_cd_1(self):
        terminal.process("cd .")
        assert terminal.cwd == TESTS_DIR

    def test_cd_2(self):
        terminal.process("cd ../.\\.")
        assert terminal.cwd == f"{Path().cwd()}\\tests"

    def test_cd_3(self):
        terminal.process("cd folder_for_tests")
        assert terminal.cwd == TESTS_DIR

    def test_cd_4(self, capsys):
        terminal.process("cd abcdef")

        captured = capsys.readouterr()
        expected = f"\033[0;31m😞 Path\033[0m \033[1;31m{TESTS_DIR}\\abcdef\033[0m \033[0;31mdoesn't exist\033[0m\n"
        assert captured.out == expected

    # cat
    def test_cat_1(self, capsys):
        terminal.process("cat somefile1.txt")

        captured = capsys.readouterr()
        expected = "text from somefile1\n"
        assert captured.out == expected

    def test_cat_2(self, capsys):
        terminal.process("cat nonexistingfile.txt")

        captured = capsys.readouterr()
        expected = f"\033[0;31m😞 Path\033[0m \033[1;31m{TESTS_DIR}\\nonexistingfile.txt\033[0m \033[0;31mdoesn't exist\033[0m\n"
        assert captured.out == expected

    def test_cat_3(self, capsys):
        terminal.process("cat subfolder_for_tests")

        captured = capsys.readouterr()
        expected = f"\033[0;31m😕 Directory path received instead of file path:\033[0m \033[1;31m{TESTS_DIR}\\subfolder_for_tests\033[0m\n"
        assert captured.out == expected

    # cp
    def test_cp_1(self):
        terminal.process("cp somefile1.txt subfolder_for_tests")
        assert access(
            path=f"{TESTS_DIR}\\subfolder_for_tests\\somefile1.txt",
            mode=F_OK,
        ) and access(path=f"{TESTS_DIR}\\somefile1.txt", mode=F_OK)

    def test_cp_2(self, capsys):
        terminal.process("cp subfolder_for_tests ..")

        captured = capsys.readouterr()
        expected = f"\033[0;31m😕 Directory path received instead of file path:\033[0m \033[1;31m{TESTS_DIR}\\subfolder_for_tests\033[0m\n"
        assert captured.out == expected

    def test_cp_3(self):
        terminal.process("cp subfolder_for_tests .. --recursive")
        assert access(
            path=f"{TESTS_DIR}\\..\\subfolder_for_tests", mode=F_OK
        ) and access(
            path=f"{TESTS_DIR}\\subfolder_for_tests",
            mode=F_OK,
        )

    # mv
    def test_mv_1(self):
        terminal.process(
            "mv subfolder_for_tests/somefile1.txt subfolder_for_tests\\somefile2.txt"
        )
        assert access(
            path=f"{TESTS_DIR}/subfolder_for_tests/somefile2.txt",
            mode=F_OK,
        ) and not access(
            path=f"{TESTS_DIR}\\subfolder_for_tests\\somefile1.txt", mode=F_OK
        )

    def test_mv_2(self, capsys):
        terminal.process("mv subfolder_for_tests .")

        captured = capsys.readouterr()
        expected = f"\033[0;31m😕 Source and destination are equal:\033[0m \033[1;31m{TESTS_DIR}\\subfolder_for_tests\033[0m\n"
        assert captured.out == expected

    def test_mv_3(self):
        terminal.process("mv subfolder_for_tests/somefile3.txt .")
        assert access(path=f"{TESTS_DIR}/somefile3.txt", mode=F_OK) and not access(
            path=f"{TESTS_DIR}/subfolder_for_tests/somefile3.txt", mode=F_OK
        )

    def test_mv_4(self):
        terminal.process("mv somefile3.txt subfolder_for_tests/.")
        assert not access(path=f"{TESTS_DIR}/somefile3.txt", mode=F_OK) and access(
            path=f"{TESTS_DIR}/subfolder_for_tests/somefile3.txt", mode=F_OK
        )

    # rm
    def test_rm_1(self):
        terminal.process("rm subfolder_for_tests/somefile2.txt")
        assert not access(
            path=f"{TESTS_DIR}/subfolder_for_tests/somefile2.txt", mode=F_OK
        ) and access(path=f"{Path().cwd()}/.trash/somefile2.txt", mode=F_OK)

    def test_rm_2(self, capsys):
        terminal.process("rm ../subfolder_for_tests")

        captured = capsys.readouterr()
        expected = f"\033[0;31m😕 Directory path received instead of file path:\033[0m \033[1;31m{Path().cwd()}\\tests\\subfolder_for_tests\033[0m\n"
        assert captured.out == expected

    def test_rm_3(self):
        terminal.process("rm -r ..\\subfolder_for_tests")
        assert not access(
            path=f"{TESTS_DIR}\\..\\subfolder_for_tests", mode=F_OK
        ) and access(path=f"{Path().cwd()}\\.trash\\subfolder_for_tests", mode=F_OK)

    def test_rm_4(self, capsys):
        terminal.process("rm ..\\.. --recursive")

        captured = capsys.readouterr()
        expected = f"\033[0;31m😡 Attempt to remove parent path:\033[0m \033[1;31m{Path().cwd()}\033[0m\n"
        assert captured.out == expected

    # zip
    def test_zip_1(self):
        terminal.process("zip subfolder_for_tests ziptest")
        assert access(path=f"{TESTS_DIR}\\ziptest.zip", mode=F_OK)

    def test_zip_2(self, capsys):
        terminal.process("zip somefile1.txt file.zip")

        captured = capsys.readouterr()
        expected = f"\033[0;31m😕 File path received instead of directory path:\033[0m \033[1;31m{TESTS_DIR}\\somefile1.txt\033[0m\n"
        assert captured.out == expected

    # unzip
    def test_unzip_1(self):
        terminal.process("unzip ziptest.zip")
        assert access(path=f"{Path().cwd()}\\subfolder_for_tests", mode=F_OK)

        terminal.process("rm ziptest.zip")
        terminal.process("rm ../../subfolder_for_tests -r")

    # tar
    def test_tar_1(self):
        terminal.process("tar subfolder_for_tests tartest")
        assert access(path=f"{TESTS_DIR}\\tartest.tar", mode=F_OK)

    def test_tar_2(self, capsys):
        terminal.process("tar somefile2.txt file.tar")

        captured = capsys.readouterr()
        expected = f"\033[0;31m😕 File path received instead of directory path:\033[0m \033[1;31m{TESTS_DIR}\\somefile2.txt\033[0m\n"
        assert captured.out == expected

    # untar
    def test_untar_1(self):
        terminal.process("untar tartest")
        assert access(path=f"{Path().cwd()}\\subfolder_for_tests", mode=F_OK)

        terminal.process("rm tartest.tar")
        terminal.process('rm ../../subfolder_for_tests -r')

    # grep
    def test_grep_1(self, capsys):
        terminal.process("grep soMEfILe2 . -r -i")

        captured = capsys.readouterr()
        expected = f'\033[0;34mFile: {TESTS_DIR}\\somefile2.txt\033[0m \033[0m\nLine 1: "somefile2" at position 10\n'
        assert captured.out == expected

    def test_grep_2(self, capsys):
        terminal.process("grep rom . --recursive")

        captured = capsys.readouterr()
        expected = f'\033[0;34mFile: {TESTS_DIR}\\somefile1.txt\033[0m \033[0m\nLine 1: "rom" at position 6\n\033[0;34mFile: {TESTS_DIR}\\somefile2.txt\033[0m \033[0m\nLine 1: "rom" at position 6\n\033[0;34mFile: {TESTS_DIR}\\subfolder_for_tests\\somefile3.txt\033[0m \033[0m\nLine 1: "rom" at position 6\n'
        assert captured.out == expected

    def test_grep_3(self, capsys):
        terminal.process("grep somefile1 subfolder_for_tests\\somefile3.txt")

        captured = capsys.readouterr()
        expected = ""
        assert captured.out == expected
