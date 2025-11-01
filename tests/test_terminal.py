import pytest
from unittest.mock import Mock
from pytest_mock import MockerFixture
from src.terminal import Terminal3000

from shutil import Error as PathAlreadyExistsError


@pytest.fixture
def utils(mocker: MockerFixture):
    yield {
        "terminal": Terminal3000(cwd="cwd", reload=False),
        "isfile": mocker.patch("src.isfile"),
        "isdir": mocker.patch("src.isdir"),
        "listdir": mocker.patch("src.listdir"),
        "getsize": mocker.patch("src.getsize"),
        "getctime": mocker.patch("src.getctime"),
        "getmtime": mocker.patch("src.getmtime"),
        "access": mocker.patch("src.access"),
        "copy": mocker.patch("src.copy"),
        "copytree": mocker.patch("src.copytree"),
        "move": mocker.patch("src.move"),
        "remove": mocker.patch("src.remove"),
        "rmtree": mocker.patch("src.rmtree"),
        "walk": mocker.patch("src.walk"),
    }


@pytest.fixture
def path(mocker: MockerFixture):
    mock = mocker.patch("src.Path")
    mocked_path = Mock()
    mocked_path.resolve.return_value = "path\\to\\somewhere"
    mocked_path.exists.return_value = True
    mock.return_value = mocked_path
    yield mock


@pytest.fixture
def fake_path(mocker: MockerFixture):
    mock = mocker.patch("src.Path")
    mocked_path = Mock()
    mocked_path.resolve.return_value = "path\\to\\somewhere"
    mocked_path.exists.return_value = False
    mock.return_value = mocked_path
    yield mock


class TestLs:

    def test_ls_fakepath(self, fake_path: Mock, utils: dict[str, Mock]):
        utils["terminal"].process("ls fakepath")

        fake_path.assert_called()
        utils["isfile"].assert_not_called()

    def test_ls_filepath(self, path: Mock, utils: dict[str, Mock]):
        utils["isfile"].return_value = True

        utils["terminal"].process("ls filepath")

        path.assert_called()
        utils["isfile"].assert_called_once()
        utils["listdir"].assert_not_called()

    def test_ls_dirpath(self, path: Mock, utils: dict[str, Mock]):
        utils["isfile"].return_value = False

        utils["terminal"].process("ls ..")

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

        utils["terminal"].process("ls --list")

        path.assert_called()
        utils["isfile"].assert_called_once()
        utils["listdir"].assert_called()


class TestCd:

    def test_cd_fakepath(self, fake_path: Mock, utils: dict[str, Mock]):
        utils["terminal"].process("cd fakepath")

        fake_path.assert_called()
        utils["isfile"].assert_not_called()

    def test_cd_home_dir(self, path: Mock, utils: dict[str, Mock]):
        utils["terminal"].process("cd ~")

        path.assert_called()
        utils["isfile"].assert_not_called()

    def test_cd_file(self, path: Mock, utils: dict[str, Mock]):
        utils["isfile"].return_value = True

        utils["terminal"].process("cd filepath")

        path.assert_called()
        utils["isfile"].assert_called_once()

    def test_cd_missing_path(self, path: Mock, utils: dict[str, Mock]):
        utils["terminal"].process("cd")

        path.assert_called()
        utils["isfile"].assert_not_called()


class TestCat:

    def test_cat_fakepath(self, fake_path: Mock, utils: dict[str, Mock]):
        utils["terminal"].process("cat fakepath")

        fake_path.assert_called()
        utils["isdir"].assert_not_called()

    def test_cat_dir(self, path: Mock, utils: dict[str, Mock], mocker: MockerFixture):
        utils["isdir"].return_value = True
        mocked_open = mocker.patch("builtins.open")

        utils["terminal"].process("cat dirpath")

        path.assert_called()
        utils["isdir"].assert_called_once()
        mocked_open.assert_not_called()

    def test_cat_success(
        self, path: Mock, utils: dict[str, Mock], mocker: MockerFixture
    ):
        utils["isdir"].return_value = False
        mocked_open = mocker.patch("builtins.open")

        utils["terminal"].process("cat textfile.txt")

        path.assert_called()
        utils["isdir"].assert_called_once()
        mocked_open.assert_called()

    def test_cat_missing_path(self, path: Mock, utils: dict[str, Mock]):
        utils["terminal"].process("cat")

        path.assert_not_called()
        utils["isdir"].assert_not_called()


class TestCp:

    def test_cp_fakepath(self, fake_path: Mock, utils: dict[str, Mock]):
        utils["terminal"].process("cp fakepath .")

        fake_path.assert_called()
        utils["isfile"].assert_not_called()
        utils["isdir"].assert_not_called()

    def test_cp_dir_without_r(
        self, path: Mock, utils: dict[str, Mock], mocker: MockerFixture
    ):
        utils["isdir"].return_value = True

        utils["terminal"].process("cp dirpath .")

        path.assert_called()
        utils["isfile"].assert_not_called()
        utils["isdir"].assert_called_once()
        utils["copy"].assert_not_called()
        utils["copytree"].assert_not_called()

    def test_cp_dir_with_r(self, path: Mock, utils: dict[str, Mock]):
        utils["isfile"].return_value = False
        utils["copytree"].return_value = "dstpath"

        utils["terminal"].process("cp dirpath . -r")

        path.assert_called()
        utils["isfile"].assert_called_once()
        utils["isdir"].assert_not_called()
        utils["copy"].assert_not_called()
        utils["copytree"].assert_called_once()

    def test_cp_file_without_r(self, path: Mock, utils: dict[str, Mock]):
        utils["isdir"].return_value = False
        utils["copy"].return_value = "dstpath"

        utils["terminal"].process("cp filepath .")

        path.assert_called()
        utils["isfile"].assert_not_called()
        utils["isdir"].assert_called_once()
        utils["copy"].assert_called_once()
        utils["copytree"].assert_not_called()

    def test_cp_file_with_r(self, path: Mock, utils: dict[str, Mock]):
        utils["isfile"].return_value = True

        utils["terminal"].process("cp filepath . --recursive")

        path.assert_called()
        utils["isfile"].assert_called_once()
        utils["isdir"].assert_not_called()
        utils["copy"].assert_not_called()
        utils["copytree"].assert_not_called()

    def test_cat_missing_args(self, path: Mock, utils: dict[str, Mock]):
        utils["terminal"].process("cp srcpathonly")

        path.assert_not_called()
        utils["isfile"].assert_not_called()
        utils["isdir"].assert_not_called()


class TestMv:

    def test_mv_fakepath(self, fake_path: Mock, utils: dict[str, Mock]):
        utils["terminal"].process("mv fakepath .")

        fake_path.assert_called()
        utils["move"].assert_not_called()
        utils["isdir"].assert_not_called()
        utils["copytree"].assert_not_called()
        utils["remove"].assert_not_called()

    def test_mv_samepath(self, path: Mock, utils: dict[str, Mock]):
        utils["terminal"].process("mv srcpath srcpath")

        path.assert_called()
        utils["move"].assert_called_once()
        utils["isdir"].assert_not_called()
        utils["copytree"].assert_not_called()
        utils["remove"].assert_not_called()

    def test_mv_dst_already_exist(self, path: Mock, utils: dict[str, Mock]):
        utils["move"].side_effect = PathAlreadyExistsError
        utils["isdir"].return_value = True

        utils["terminal"].process("mv srcpath dirpath")

        path.assert_called()
        utils["move"].assert_called_once()
        utils["isdir"].assert_called_once()
        utils["copy"].assert_not_called()
        utils["copytree"].assert_called_once()
        utils["remove"].assert_not_called()
        utils["rmtree"].assert_called_once()

    def test_mv_missing_args(self, path: Mock, utils: dict[str, Mock]):
        utils["terminal"].process("mv srcpathonly")

        path.assert_not_called()
        utils["move"].assert_not_called()
        utils["isdir"].assert_not_called()
        utils["copytree"].assert_not_called()
        utils["remove"].assert_not_called()


class TestRm:

    def test_rm_fakepath(self, fake_path: Mock, utils: dict[str, Mock]):
        utils["terminal"].process("rm fakepath")

        fake_path.assert_called()
        utils["move"].assert_not_called()
        utils["isfile"].assert_not_called()
        utils["isdir"].assert_not_called()
        utils["move"].assert_not_called()
        utils["remove"].assert_not_called()
        utils["rmtree"].assert_not_called()

    def test_rm_dirpath_without_r(self, path: Mock, utils: dict[str, Mock]):
        utils["isdir"].return_value = True

        utils["terminal"].process("rm dirpath")

        path.assert_called()
        utils["isfile"].assert_not_called()
        utils["isdir"].assert_called_once()
        utils["move"].assert_not_called()
        utils["remove"].assert_not_called()
        utils["rmtree"].assert_not_called()

    def test_rm_dirpath_with_r(
        self, path: Mock, utils: dict[str, Mock], mocker: MockerFixture
    ):
        utils["isfile"].return_value = False
        utils["copytree"].return_value = "dstpath"
        utils["rmtree"].return_value = None
        mocked_confirmation = mocker.patch.object(
            utils["terminal"].commands["rm"], "get_confirmation"
        )
        mocked_confirmation.return_value = True

        utils["terminal"].process("rm dirpath -r")

        path.assert_called()
        utils["isfile"].assert_called_once()
        utils["isdir"].assert_not_called()
        utils["move"].assert_called_once()
        utils["rmtree"].assert_not_called()

    def test_rm_filepath_without_r(self, path: Mock, utils: dict[str, Mock]):
        utils["isdir"].return_value = False

        utils["terminal"].process("rm filepath")

        path.assert_called()
        utils["isfile"].assert_not_called()
        utils["isdir"].assert_called_once()
        utils["move"].assert_called_once()
        utils["remove"].assert_not_called()

    def test_rm_filepath_with_r(self, path: Mock, utils: dict[str, Mock]):
        utils["isfile"].return_value = True

        utils["terminal"].process("rm filepath --recursive")

        path.assert_called()
        utils["isfile"].assert_called_once()
        utils["isdir"].assert_not_called()
        utils["move"].assert_not_called()
        utils["remove"].assert_not_called()
        utils["rmtree"].assert_not_called()

    def test_rm_dirpath_already_exists_error(
        self, path: Mock, utils: dict[str, Mock], mocker: MockerFixture
    ):
        utils["move"].side_effect = [PathAlreadyExistsError, None]
        utils["isfile"].return_value = False
        mocked_confirmation = mocker.patch.object(
            utils["terminal"].commands["rm"], "get_confirmation"
        )
        mocked_confirmation.return_value = True

        utils["terminal"].process("rm dirpath -r")

        path.assert_called()
        utils["isfile"].assert_called_once()
        utils["isdir"].assert_not_called()
        utils["move"].assert_called()
        utils["remove"].assert_not_called()
        utils["rmtree"].assert_called_once()

    def test_rm_filepath_already_exists_error(self, path: Mock, utils: dict[str, Mock]):
        utils["move"].side_effect = [PathAlreadyExistsError, None]
        utils["isdir"].return_value = False

        utils["terminal"].process("rm filepath")

        path.assert_called()
        utils["isfile"].assert_not_called()
        utils["isdir"].assert_called_once()
        utils["move"].assert_called()
        utils["remove"].assert_called_once()
        utils["rmtree"].assert_not_called()

    def test_rm_missing_arg(self, path: Mock, utils: dict[str, Mock]):
        utils["terminal"].process("rm")

        path.assert_not_called()
        utils["isfile"].assert_not_called()
        utils["isdir"].assert_not_called()
        utils["move"].assert_not_called()
        utils["rmtree"].assert_not_called()
        utils["remove"].assert_not_called()


class TestZip:

    def test_zip_fakepath(
        self, fake_path: Mock, utils: dict[str, Mock], mocker: MockerFixture
    ):
        mocked_zipfile = mocker.patch("src.commands.zip.ZipFile")

        utils["terminal"].process("zip fakepath")

        fake_path.assert_called()
        utils["isfile"].assert_not_called()
        mocked_zipfile.assert_not_called()

    def test_zip_dirpath(
        self, path: Mock, utils: dict[str, Mock], mocker: MockerFixture
    ):
        mocked_zipfile = mocker.patch("src.commands.zip.ZipFile")
        utils["isfile"].return_value = False

        utils["terminal"].process("zip dirpath arcname")

        path.assert_called()
        utils["isfile"].assert_called_once()
        mocked_zipfile.assert_called_once()

    def test_zip_filepath(
        self, path: Mock, utils: dict[str, Mock], mocker: MockerFixture
    ):
        mocked_zipfile = mocker.patch("src.commands.zip.ZipFile")
        utils["isfile"].return_value = True

        utils["terminal"].process("zip filepath arcname")

        path.assert_called()
        utils["isfile"].assert_called_once()
        mocked_zipfile.assert_not_called()

    def test_zip_missing_arg(
        self, path: Mock, utils: dict[str, Mock], mocker: MockerFixture
    ):
        mocked_zipfile = mocker.patch("src.commands.zip.ZipFile")

        utils["terminal"].process("zip")

        path.assert_not_called()
        utils["isfile"].assert_not_called()
        mocked_zipfile.assert_not_called()


class TestTar:

    def test_tar_fakepath(
        self, fake_path: Mock, utils: dict[str, Mock], mocker: MockerFixture
    ):
        mocked_tarfile = mocker.patch("src.commands.tar.TarFile")

        utils["terminal"].process("tar fakepath")

        fake_path.assert_called()
        utils["isfile"].assert_not_called()
        mocked_tarfile.assert_not_called()

    def test_tar_dirpath(
        self, path: Mock, utils: dict[str, Mock], mocker: MockerFixture
    ):
        mocked_tarfile = mocker.patch("src.commands.tar.TarFile")
        utils["isfile"].return_value = False

        utils["terminal"].process("tar dirpath arcname")

        path.assert_called()
        utils["isfile"].assert_called_once()
        mocked_tarfile.assert_called_once()

    def test_tar_filepath(
        self, path: Mock, utils: dict[str, Mock], mocker: MockerFixture
    ):
        mocked_tarfile = mocker.patch("src.commands.tar.TarFile")
        utils["isfile"].return_value = True

        utils["terminal"].process("tar filepath arcname")

        path.assert_called()
        utils["isfile"].assert_called_once()
        mocked_tarfile.assert_not_called()

    def test_tar_missing_arg(
        self, path: Mock, utils: dict[str, Mock], mocker: MockerFixture
    ):
        mocked_tarfile = mocker.patch("src.commands.tar.TarFile")

        utils["terminal"].process("tar")

        path.assert_not_called()
        utils["isfile"].assert_not_called()
        mocked_tarfile.assert_not_called()


class TestUnzip:

    def test_unzip_fakepath(
        self, fake_path: Mock, utils: dict[str, Mock], mocker: MockerFixture
    ):
        mocked_iszipfile = mocker.patch("src.commands.unzip.is_zipfile")
        mocked_zipfile = mocker.patch("src.commands.unzip.ZipFile")

        utils["terminal"].process("unzip fakepath")

        fake_path.assert_called()
        mocked_iszipfile.assert_not_called()
        mocked_zipfile.assert_not_called()

    def test_unzip_not_zipfile(
        self, path: Mock, utils: dict[str, Mock], mocker: MockerFixture
    ):
        mocked_iszipfile = mocker.patch("src.commands.unzip.is_zipfile")
        mocked_iszipfile.return_value = False
        mocked_zipfile = mocker.patch("src.commands.unzip.ZipFile")

        utils["terminal"].process("unzip notzipfile")

        path.assert_called()
        mocked_iszipfile.assert_called_once()
        mocked_zipfile.assert_not_called()

    def test_unzip_success(
        self, path: Mock, utils: dict[str, Mock], mocker: MockerFixture
    ):
        mocked_iszipfile = mocker.patch("src.commands.unzip.is_zipfile")
        mocked_iszipfile.return_value = True
        mocked_zipfile = mocker.patch("src.commands.unzip.ZipFile")

        utils["terminal"].process("unzip zipfile")

        path.assert_called()
        mocked_iszipfile.assert_called_once()
        mocked_zipfile.assert_called_once()

    def test_unzip_missing_arg(
        self, path: Mock, utils: dict[str, Mock], mocker: MockerFixture
    ):
        mocked_iszipfile = mocker.patch("src.commands.unzip.is_zipfile")
        mocked_zipfile = mocker.patch("src.commands.unzip.ZipFile")

        utils["terminal"].process("unzip")

        path.assert_not_called()
        mocked_iszipfile.assert_not_called()
        mocked_zipfile.assert_not_called()


class TestUntar:

    def test_untar_fakepath(
        self, fake_path: Mock, utils: dict[str, Mock], mocker: MockerFixture
    ):
        mocked_istarfile = mocker.patch("src.commands.untar.is_tarfile")
        mocked_tarfile = mocker.patch("src.commands.untar.TarFile")

        utils["terminal"].process("untar fakepath")

        fake_path.assert_called()
        mocked_istarfile.assert_not_called()
        mocked_tarfile.assert_not_called()

    def test_untar_not_zipfile(
        self, path: Mock, utils: dict[str, Mock], mocker: MockerFixture
    ):
        mocked_istarfile = mocker.patch("src.commands.untar.is_tarfile")
        mocked_istarfile.return_value = False
        mocked_tarfile = mocker.patch("src.commands.untar.TarFile")

        utils["terminal"].process("untar nottarfile")

        path.assert_called()
        mocked_istarfile.assert_called_once()
        mocked_tarfile.assert_not_called()

    def test_untar_success(
        self, path: Mock, utils: dict[str, Mock], mocker: MockerFixture
    ):
        mocked_istarfile = mocker.patch("src.commands.untar.is_tarfile")
        mocked_istarfile.return_value = True
        mocked_tarfile = mocker.patch("src.commands.untar.TarFile")

        utils["terminal"].process("untar tarfile")

        path.assert_called()
        mocked_istarfile.assert_called_once()
        mocked_tarfile.assert_called_once()

    def test_untar_missing_arg(
        self, path: Mock, utils: dict[str, Mock], mocker: MockerFixture
    ):
        mocked_istarfile = mocker.patch("src.commands.untar.is_tarfile")
        mocked_tarfile = mocker.patch("src.commands.untar.TarFile")

        utils["terminal"].process("untar")

        path.assert_not_called()
        mocked_istarfile.assert_not_called()
        mocked_tarfile.assert_not_called()


class TestGrep:

    def test_grep_fakepath(self, fake_path: Mock, utils: dict[str, Mock]):
        utils["terminal"].process("grep pattern fakepath")

        fake_path.assert_called()
        utils["isfile"].assert_not_called()
        utils["listdir"].assert_not_called()
        utils["walk"].assert_not_called()

    def test_grep_filepath_without_r(
        self, path: Mock, utils: dict[str, Mock], mocker: MockerFixture
    ):
        utils["isfile"].return_value = True
        mocked_search = mocker.patch.object(
            utils["terminal"].commands["grep"], "search_pattern"
        )

        utils["terminal"].process("grep pattern filepath")

        path.assert_called()
        utils["isfile"].assert_called_once()
        mocked_search.assert_called_once()
        utils["listdir"].assert_not_called()
        utils["walk"].assert_not_called()

    def test_grep_filepath_with_r(
        self, path: Mock, utils: dict[str, Mock], mocker: MockerFixture
    ):
        utils["isfile"].return_value = True
        mocked_search = mocker.patch.object(
            utils["terminal"].commands["grep"], "search_pattern"
        )

        utils["terminal"].process("grep pattern filepath -r")

        path.assert_called()
        utils["isfile"].assert_called_once()
        mocked_search.assert_not_called()
        utils["listdir"].assert_not_called()
        utils["walk"].assert_not_called()

    def test_grep_dirpath_without_r(self, path: Mock, utils: dict[str, Mock]):
        utils["isfile"].return_value = False

        utils["terminal"].process("grep pattern dirpath")

        path.assert_called()
        utils["isfile"].assert_called_once()
        utils["listdir"].assert_called_once()
        utils["walk"].assert_not_called()

    def test_grep_dirpath_with_r(self, path: Mock, utils: dict[str, Mock]):
        utils["isfile"].return_value = False

        utils["terminal"].process("grep pattern dirpath -r")

        path.assert_called()
        utils["isfile"].assert_called_once()
        utils["listdir"].assert_not_called()
        utils["walk"].assert_called_once()

    def test_grep_missing_args(self, path: Mock, utils: dict[str, Mock]):
        utils["terminal"].process("grep onlypattern")

        path.assert_not_called()
        utils["isfile"].assert_not_called()
        utils["listdir"].assert_not_called()
        utils["walk"].assert_not_called()


class TestHistory:

    def test_history_not_exists(
        self, fake_path: Mock, utils: dict[str, Mock], mocker: MockerFixture
    ):
        mocked_open = mocker.patch("builtins.open")

        utils["terminal"].process("history")

        fake_path.assert_called()
        mocked_open.assert_not_called()

    def test_history_success(
        self, path: Mock, utils: dict[str, Mock], mocker: MockerFixture
    ):
        mocked_open = mocker.patch("builtins.open")

        utils["terminal"].process("history --count 20")

        path.assert_called()
        mocked_open.assert_called()


class TestUndo:

    def test_undo_history_not_exists(self, fake_path: Mock, utils: dict[str, Mock], mocker: MockerFixture):
        mocked_open = mocker.patch('builtins.open')

        utils['terminal'].process('undo')

        fake_path.assert_called()
        mocked_open.assert_not_called()

    def test_undo_not_found_commands(self, path: Mock, utils: dict[str, Mock], mocker: MockerFixture):
        mocked_open = mocker.patch('builtins.open')
        mocked_open.readlines.return_value = ['New session ...']
        mocked_message = mocker.patch('src.errors.command_to_undo_not_found_message')

        utils['terminal'].process('undo')

        path.assert_called()
        mocked_message.assert_called_once()
