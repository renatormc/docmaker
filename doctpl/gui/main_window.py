from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QComboBox, QMessageBox
from doctpl.gui.form import BaseForm
from typing import Type
from pathlib import Path
from doctpl.renderer import Renderer


class MainWindow(QMainWindow):
    def __init__(self, forms: list[Type[BaseForm]], dest_dir: str | Path) -> None:
        self.forms = forms
        self.dest_dir = Path(dest_dir)
        super(self.__class__, self).__init__()
        self.setup_ui()
        self.connections()
        self.current_form = self.load_model(0)

    def setup_ui(self):
        self.main_layout = QVBoxLayout()
        w = QWidget()
        w.setLayout(self.main_layout)
        self.setCentralWidget(w)

        self.cbx_form = QComboBox()
        for f in self.forms:
            self.cbx_form.addItem(f.name)
        self.main_layout.addWidget(self.cbx_form)

    def connections(self):
        self.cbx_form.currentTextChanged.connect(self.change_model)

    def change_model(sel, value):
        print(value)

    def load_model(self, index: int) -> BaseForm:
        f = self.forms[index]()
        self.main_layout.addWidget(f)
        return f

    def render(self):
        context, errors = self.current_form.get_context()
        if errors:
            QMessageBox.warning(self, "Erro de formulário",
                                "Há erros em seu formulário. Corrija-os antes de prosseguir.")
            return
        r = Renderer(self.current_form.templates_dir)
        try:
            r.pre_render("main.odt", self.dest_dir, overwrite=True, **context)
        except Exception as e:
            QMessageBox.warning(self, "Erro", str(e))
