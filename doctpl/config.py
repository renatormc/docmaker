from pathlib import Path
import os
from doctpl.custom_types import EnvType

LIBDIR = Path(os.path.dirname(os.path.realpath(__file__)))


class Config:
    def __init__(self) -> None:
        self.env: EnvType = "prod"
        self._local_folder: Path = Path("./local")
        self._tempdir = self.local_folder / "tmp"
        self.loffice_exe = "soffice"

    @property
    def local_folder(self) -> Path:
        return self._local_folder
    
    @local_folder.setter
    def local_folder(self, value: str | Path) -> None:
        self._local_folder = Path(value)
        self._tempdir = self._local_folder / "tmp"
        try:
            self._tempdir.mkdir()
        except FileExistsError:
            pass

    @property
    def tempdir(self) -> Path:
        return self._tempdir


_config = Config()


def get_config() -> Config:
    return _config
