import os
from pathlib import Path

from aio_concurrent.functions import chmod, chown, rm

BASE_DIR = Path(__file__).resolve().parent

ASSERTS = str(BASE_DIR / "assets/**")

ASSERTS_TXT = str(BASE_DIR / "assets/**/*.txt")


def test_chmod(mocker):
    mocker.patch("os.chmod")
    chmod(ASSERTS, mode=0o777)("/path/to/file")
    os.chmod.assert_called_once_with("/path/to/file", 0o777)


def test_chown(mocker):
    mocker.patch("os.chown")
    chown(ASSERTS, uid=1, gid=1)("/path/to/file")
    os.chown.assert_called_once_with("/path/to/file", 1, 1)


def test_rm(mocker):
    mocker.patch("os.path.isdir", return_value=True)
    mocker.patch("os.rmdir")
    rm(ASSERTS)("/path/to/file")
    os.rmdir.assert_called_once_with("/path/to/file")

    mocker.patch("os.path.isdir", return_value=False)
    mocker.patch("os.remove")
    rm(ASSERTS)("/path/to/file")
    os.remove.assert_called_once_with("/path/to/file")


def test_get_items():
    assert len(chmod(ASSERTS, mode=0o777).get_items()) == 6

    assert len(chmod(ASSERTS, f"!{ASSERTS_TXT}", mode=0o777).get_items()) == 3
