from doctpl.docmodel import DocModel
from PySide6.QtWidgets import QApplication
from doctpl.gui.main_window import MainWindow
import sys
from doctpl.config import get_config
from pathlib import Path
from doctpl.custom_types import EnvType
from doctpl import repo
from doctpl.gui.helpers import get_icon

class App:
    def __init__(self, local_folder: str | Path,
                 docmodels: list[DocModel] = [],
                 env: EnvType | None = None) -> None:
        self.docmodels = docmodels
        self.set_local_folder(local_folder)
        if env:
            self.set_env(env)
        repo.connect(local_folder / "db.json")
        

    def add_docmodel(self, m: DocModel) -> None:
        self.docmodels.append(m)

    def set_local_folder(self, local_folder: str | Path) -> None:
        cf = get_config()
        cf.local_folder = local_folder

    def set_env(self, env: EnvType) -> None:
        cf = get_config()
        cf.env = env

    def run_gui(self) -> None:
        app = QApplication(sys.argv)
        w = MainWindow(self.docmodels)
        app.setWindowIcon(get_icon("writer.png"))
        w.show()
        sys.exit(app.exec())
