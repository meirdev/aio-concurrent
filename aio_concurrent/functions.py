import glob
import os
from abc import ABC, abstractmethod


class BaseFunction(ABC):
    @abstractmethod
    def get_items(self) -> list[str]:  # pragma: no cover
        ...

    @abstractmethod
    def __call__(self, item: str) -> None:  # pragma: no cover
        ...


class IOBaseFunction(BaseFunction, ABC):
    def __init__(self, *path: str) -> None:
        self._path = path

    def get_items(self) -> list[str]:
        def _glob(path: str) -> set[str]:
            return set(map(os.path.realpath, glob.iglob(path, recursive=True)))  # type: ignore[arg-type]

        paths: set[str] = set()

        for i in self._path:
            if i.startswith("!"):
                paths -= _glob(i[1:])
            else:
                paths |= _glob(i)

        return sorted(paths, reverse=True)


class chmod(IOBaseFunction):
    def __init__(self, *path: str, mode: int) -> None:
        super().__init__(*path)

        self._mode = mode

    def __call__(self, file: str) -> None:
        os.chmod(file, self._mode)


class chown(IOBaseFunction):
    def __init__(self, *path: str, uid: int, gid: int) -> None:
        super().__init__(*path)

        self._uid = uid
        self._gid = gid

    def __call__(self, file: str) -> None:
        os.chown(file, self._uid, self._gid)


class rm(IOBaseFunction):
    def __call__(self, file: str) -> None:
        if os.path.isdir(file):
            os.rmdir(file)
        else:
            os.remove(file)
