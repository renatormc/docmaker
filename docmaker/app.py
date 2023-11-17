from docmaker.docmodel import DocModel
from PySide6.QtWidgets import QApplication
from docmaker.gui.main_window import MainWindow
import sys
from docmaker.config import get_config
from docmaker.custom_types import EnvType
from docmaker import repo

class App:
    def __init__(self,docmodels: list[DocModel] = [],
                 env: EnvType | None = None,
                 loffice_exe: str | None = None,
                 open_file_after_render = True) -> None:
        self.docmodels = docmodels
        if env:
            self.set_env(env)
        cf = get_config()
        cf.open_file_after_render = open_file_after_render
        if loffice_exe:
            cf.loffice_exe = loffice_exe
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
