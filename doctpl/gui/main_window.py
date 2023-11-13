from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QComboBox, QMessageBox, QPushButton, QFileDialog, QDialog
from doctpl.gui.form import BaseForm
from typing import Type
from pathlib import Path
from doctpl.renderer import Renderer
from doctpl.gui.helpers import spacer, get_icon
from doctpl.helpers import open_doc, open_in_filemanager
from doctpl.writer_handler import WriterHandler
import config
from uuid import uuid4
import shutil

class MainWindow(QMainWindow):
    def __init__(self, forms: list[Type[BaseForm]]) -> None:
        self.forms = {f.name: f for f in forms}
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
        
        self.create_buttons()

        self.setWindowIcon(get_icon("writer.png"))
        self.setWindowTitle("DocTpl")
        self.resize(800, 600)

    def create_buttons(self):
        self.lay_buttons = QHBoxLayout()
        self.lay_buttons.addSpacerItem(spacer("horizontal"))

        
        self.btn_open_templates = QPushButton("Templates")
        self.btn_open_templates.setMinimumHeight(45)
        self.btn_open_templates.setMinimumWidth(120)
        self.lay_buttons.addWidget(self.btn_open_templates)


        self.btn_open_writer = QPushButton("Abrir Writer")
        self.btn_open_writer.setMinimumHeight(45)
        self.btn_open_writer.setMinimumWidth(120)
        self.lay_buttons.addWidget(self.btn_open_writer)

        self.btn_render_file = QPushButton("Renderizar arquivo")
        self.btn_render_file.setMinimumHeight(45)
        self.btn_render_file.setMinimumWidth(120)
        self.lay_buttons.addWidget(self.btn_render_file)

    
        self.btn_render_writer = QPushButton("Renderizar no Writer")
        self.btn_render_writer.setMinimumHeight(45)
        self.btn_render_writer.setMinimumWidth(120)
        self.lay_buttons.addWidget(self.btn_render_writer)

        self.main_layout.addLayout(self.lay_buttons)

    def connections(self):
        self.cbx_form.currentTextChanged.connect(self.change_model)
        self.btn_render_file.clicked.connect(self.render_file)
        self.btn_render_writer.clicked.connect(self.render_to_writer)
        self.btn_open_templates.clicked.connect(self.open_templates)

    def change_model(self, value):
        self.load_model(value)

    def load_model(self, name: str) -> None:
        if self.current_form is not None:
            self.current_form.deleteLater()
        self.current_form = self.forms[name]()
        self.lay_form.addWidget(self.current_form)


    def render_file(self):
        context, errors = self.current_form.get_context()
        if errors:
            QMessageBox.warning(self, "Erro de formulário",
                                "Há erros em seu formulário. Corrija-os antes de prosseguir.")
            return
        file_dialog = QFileDialog()
        file_dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)
        file_dialog.setNameFilter("ODT Files (*.odt)")
        file_dialog.setDefaultSuffix("odt")
        file_dialog.setDirectory(str(Path(".").absolute()))

        if file_dialog.exec_():
            selected_file = Path(file_dialog.selectedFiles()[0])
            renderer = Renderer(self.current_form.templates_dir)
            try:
                renderer.pre_render("main.odt", selected_file, overwrite=True, **context)
                open_doc(selected_file)
                QMessageBox.information(self, "Pós processamento",
                                "Aguarde o documento terminar de ser aberto no Writer e clique em OK.")
                wh = WriterHandler()
                wh.run_macro("pos_process", str(renderer.render_files.files_dir))
                self.close()
            except Exception as e:
                QMessageBox.warning(self, "Erro", str(e))
            finally:
                try:
                    shutil.rmtree(renderer.render_files.files_dir)
                except FileNotFoundError:
                    pass
                         
    def open_templates(self):
        open_in_filemanager(self.current_form.templates_dir)

    def render_to_writer(self):
        context, errors = self.current_form.get_context()
        if errors:
            QMessageBox.warning(self, "Erro de formulário",
                                "Há erros em seu formulário. Corrija-os antes de prosseguir.")
            return
        context = self.current_form.pre_process(context)
        path = config.TEMPDIR / f"{uuid4().hex}.odt"
        renderer = Renderer(self.current_form.templates_dir)
        try:
            renderer.pre_render("main.odt", path, overwrite=True, **context)
            wh = WriterHandler()
            wh.run_macro("add_doc", str(path))
            wh.run_macro("pos_process", str(renderer.render_files.files_dir))
            self.close()
        except Exception as e:
            QMessageBox.warning(self, "Erro", str(e))
        finally:
            try:
                shutil.rmtree(renderer.render_files.files_dir)
            except FileNotFoundError:
                pass
            try:
                path.unlink()
            except FileNotFoundError:
                pass
