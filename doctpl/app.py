from doctpl.docmodel import DocModel
from PySide6.QtWidgets import QApplication
from doctpl.gui.main_window import MainWindow
import sys

class App:
    def __init__(self, docmodels: list[DocModel] = []) -> None:
        self.docmodels = docmodels

    def add_docmodel(self, m: DocModel) -> None:
        self.docmodels.append(m)

    def run_gui(self) -> None:
        app = QApplication(sys.argv)
        w = MainWindow(self.docmodels)
        w.show()
        sys.exit(app.exec())