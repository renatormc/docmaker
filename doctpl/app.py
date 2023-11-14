from doctpl.docmodel import DocModel
from PySide6.QtWidgets import QApplication
from doctpl.gui.main_window import MainWindow
import sys
from doctpl.config import get_config
from pathlib import Path
from doctpl.custom_types import EnvType
from doctpl import repo

class App:
    def __init__(self, local_folder: str | Path,
                 loffice_exe: str,
                 docmodels: list[DocModel] = [],
                 env: EnvType | None = None) -> None:
        self.docmodels = docmodels
        self.set_local_folder(local_folder)
        if env:
            self.set_env(env)

        self.set_loffice_exe(loffice_exe)
        repo.connect(local_folder / "db.json")
        

    def add_docmodel(self, m: DocModel) -> None:
        self.docmodels.append(m)

    def set_local_folder(self, local_folder: str | Path) -> None:
        cf = get_config()
        cf.local_folder = local_folder

    def set_env(self, env: EnvType) -> None:
        cf = get_config()
        cf.env = env

    def set_loffice_exe(self, value: str) -> None:
        cf = get_config()
        cf.loffice_exe = value

    def run_gui(self) -> None:
        app = QApplication(sys.argv)
        w = MainWindow(self.docmodels)
        w.show()
        sys.exit(app.exec())
