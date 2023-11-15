from doctpl.docmodel import DocModel
from PySide6.QtWidgets import QApplication
from doctpl.gui.main_window import MainWindow
import sys
from doctpl.config import get_config
from doctpl.custom_types import EnvType
from doctpl import repo

class App:
    def __init__(self,docmodels: list[DocModel] = [],
                 env: EnvType | None = None) -> None:
        self.docmodels = docmodels
        if env:
            self.set_env(env)
        cf = get_config()
        repo.connect(cf.local_folder / "db.json")
        

    def add_docmodel(self, m: DocModel) -> None:
        self.docmodels.append(m)

    def set_env(self, env: EnvType) -> None:
        cf = get_config()
        cf.env = env

    def run_gui(self) -> None:
        app = QApplication(sys.argv)
        w = MainWindow(self.docmodels)
        w.show()
        sys.exit(app.exec())
