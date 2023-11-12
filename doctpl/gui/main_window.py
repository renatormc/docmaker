from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QComboBox, QMessageBox, QPushButton
from doctpl.gui.form import BaseForm
from typing import Type
from pathlib import Path
from doctpl.renderer import Renderer
from doctpl.gui.helpers import spacer, get_icon
import logging


class MainWindow(QMainWindow):
    def __init__(self, forms: list[Type[BaseForm]], dest_dir: str | Path) -> None:
        self.forms = {f.name: f for f in forms}
        self.dest_dir = Path(dest_dir)
        super(self.__class__, self).__init__()
        self.setup_ui()
        self.connections()
        self.current_form: BaseForm | None = None
        self.load_model(forms[0].name)

    def setup_ui(self):
        self.main_layout = QVBoxLayout()
        w = QWidget()
        w.setLayout(self.main_layout)
        self.setCentralWidget(w)

        self.cbx_form = QComboBox()
        for name in self.forms.keys():
            self.cbx_form.addItem(name)
        self.main_layout.addWidget(self.cbx_form)
        self.lay_form = QVBoxLayout()
        self.main_layout.addLayout(self.lay_form)
        
        self.lay_buttons = QHBoxLayout()
        self.btn_ok = QPushButton("OK")
        
        self.lay_buttons.addSpacerItem(spacer("horizontal"))
        self.main_layout.addLayout(self.lay_buttons)
        self.lay_buttons.addWidget(self.btn_ok)

        self.setWindowIcon(get_icon("writer.png"))
        self.setWindowTitle("DocTpl")
        self.resize(800, 600)

    def connections(self):
        self.cbx_form.currentTextChanged.connect(self.change_model)
        self.btn_ok.clicked.connect(self.render)

    def change_model(self, value):
        self.load_model(value)

    def load_model(self, name: str) -> None:
        if self.current_form is not None:
            self.current_form.deleteLater()
        self.current_form = self.forms[name]()
        self.lay_form.addWidget(self.current_form)


    def render(self):
        context, errors = self.current_form.get_context()
        if errors:
            QMessageBox.warning(self, "Erro de formulário",
                                "Há erros em seu formulário. Corrija-os antes de prosseguir.")
            return
        
        logging.info(f"templates_dir: {self.current_form.templates_dir}")
        r = Renderer(self.current_form.templates_dir)
        try:
            r.pre_render("main.odt", self.dest_dir, overwrite=True, **context)
            self.close()
        except Exception as e:
            QMessageBox.warning(self, "Erro", str(e))
