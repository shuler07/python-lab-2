import pytest
from unittest.mock import Mock
from pytest_mock import MockerFixture
from src.terminal import Terminal3000

terminal = Terminal3000(reload=False)


@pytest.fixture
def utils(mocker: MockerFixture):
    yield {
        "isfile": mocker.patch("src.isfile"),
        "isdir": mocker.patch('src.isdir'),
        "listdir": mocker.patch("src.listdir"),
        "getsize": mocker.patch("src.getsize"),
        "getctime": mocker.patch("src.getctime"),
        "getmtime": mocker.patch("src.getmtime"),
        "access": mocker.patch("src.access"),
    }


@pytest.fixture
def path(mocker: MockerFixture):
    mock = mocker.patch("src.Path")
    mocked_path = Mock()
    mocked_path.resolve.return_value = ''
    mocked_path.exists.return_value = True
    mock.return_value = mocked_path
    yield mock


@pytest.fixture
def fake_path(mocker: MockerFixture):
    mock = mocker.patch("src.Path")
    mocked_path = Mock()
    mocked_path.resolve.return_value = ''
    mocked_path.exists.return_value = False
    mock.return_value = mocked_path
    yield mock


class TestLs:

    def test_ls_fakepath(self, fake_path: Mock, utils: dict[str, Mock]):
        terminal.process('ls fakepath')

        fake_path.assert_called()
        utils["isfile"].assert_not_called()

    def test_ls_filepath(self, path: Mock, utils: dict[str, Mock]):
        utils["isfile"].return_value = True

        terminal.process("ls filepath")

        path.assert_called()
        utils["isfile"].assert_called_once()
        utils["listdir"].assert_not_called()

    def test_ls_dirpath(self, path: Mock, utils: dict[str, Mock]):
        utils["isfile"].return_value = False

        terminal.process("ls ..")

        path.assert_called()
        utils["isfile"].assert_called_once()
        utils["listdir"].assert_called_once()

    def test_ls_list_flag(self, path: Mock, utils: dict[str, Mock]):
        utils["isfile"].return_value = False
        utils["listdir"].return_value = ["file1", "file2"]
        utils["getsize"].return_value = 20
        utils["getctime"].return_value = 1609459200
        utils["getmtime"].return_value = 1609459200
        utils["access"].return_value = True

        terminal.process("ls --list")

        path.assert_called()
        utils["isfile"].assert_called_once()
        utils["listdir"].assert_called()


class TestCd:

    def test_cd_fakepath(self, fake_path: Mock, utils: dict[str, Mock]):
        terminal.process("cd fakepath")

        fake_path.assert_called()
        utils["isfile"].assert_not_called()

    def test_cd_home_dir(self, path: Mock, utils: dict[str, Mock]):
        terminal.process('cd ~')

        path.assert_called_once()

    def test_cd_file(self, path: Mock, utils: dict[str, Mock]):
        utils["isfile"].return_value = True

        terminal.process('cd filepath')

        path.assert_called()
        utils['isfile'].assert_called_once()

    def test_cd_missing_path(self, path: Mock, utils: dict[str, Mock]):
        terminal.process('cd')

        path.assert_called()
        utils['isfile'].assert_not_called()


class TestCat:

    def test_cat_fakepath(self, fake_path: Mock, utils: dict[str, Mock]):
        terminal.process('cat fakepath')

        fake_path.assert_called()
        utils['isdir'].assert_not_called()

    def test_cat_dir(self, path: Mock, utils: dict[str, Mock], mocker: MockerFixture):
        utils['isdir'].return_value = True
        mocked_open = mocker.patch('builtins.open')

        terminal.process('cat dirpath')

        path.assert_called()
        utils['isdir'].assert_called_once()
        mocked_open.assert_not_called()

    def test_cat_success(self, path: Mock, utils: dict[str, Mock], mocker: MockerFixture):
        utils['isdir'].return_value = False
        mocked_open = mocker.patch('builtins.open')

        terminal.process('cat textfile.txt')

        path.assert_called()
        utils['isdir'].assert_called_once()
        mocked_open.assert_called()

    def test_cat_missing_path(self, path: Mock, utils: dict[str, Mock]):
        terminal.process('cat')

        path.assert_not_called()
        utils['isdir'].assert_not_called()


class TestCp:
    ...
