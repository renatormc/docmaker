from pathlib import Path
import os
from doctpl.custom_types import EnvType

LIBDIR = Path(os.path.dirname(os.path.realpath(__file__)))


class Config:
    def __init__(self) -> None:
        self.env: EnvType = "prod"
        aux = os.getenv("DOCTPL_LOCAL_FOLDER")
        self.local_folder = Path(aux) if aux else Path.home() / ".doctpl"
        try:
            self.local_folder.mkdir(parents=True)
        except FileExistsError:
            pass
        self.tempdir = self.local_folder / "tmp"
        try:
            self.tempdir.mkdir()
        except FileExistsError:
            pass
        self.loffice_exe = "C:\\Program Files\\LibreOffice\\program\\soffice.exe" if os.name == "nt" else "soffice"


_config = Config()


def get_config() -> Config:
    return _config
