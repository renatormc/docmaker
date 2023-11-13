from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QComboBox, QMessageBox, QPushButton, QFileDialog
from PySide6.QtCore import QSize
from doctpl.gui.form import BaseForm
from typing import Type
from pathlib import Path
from doctpl.renderer import Renderer
from doctpl.gui.helpers import spacer, get_icon
from doctpl.helpers import open_writer, open_in_filemanager
from doctpl.writer_handler import WriterHandler
import config
from uuid import uuid4
import shutil
import traceback
import repo
from doctpl.custom_types import Context


class MainWindow(QMainWindow):
    def __init__(self, forms: list[Type[BaseForm]]) -> None:
        self.forms = {f.name: f for f in forms}
        super(self.__class__, self).__init__()
        self.setup_ui()
        self.connections()
        self.current_form: BaseForm | None = None
        self.load_last()


    def load_form(self, name: str, context: Context | None = None) -> None:
        if self.current_form is not None:
            self.current_form.deleteLater()
        self.current_form = self.forms[name]()
        if context:
            self.current_form.load(context)
        else:
            self.current_form.load_last_context()
        self.lay_form.addWidget(self.current_form)
        self.cbx_form.setCurrentText(name)

    def load_last(self):
        last_context = repo.get_last_context()
        
        if last_context:
            try:
                form = self.forms[last_context["model_name"]]
                print(last_context["model_name"])
                self.load_form(form.name, last_context["context"])
                return
            except KeyError:
                pass
        else:
            name = [name for name in self.forms.keys()][0]
            self.load_form(name)
        
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
        self.resize(1000, 800)

    def create_buttons(self):
        self.lay_buttons = QHBoxLayout()
        self.lay_buttons.addSpacerItem(spacer("horizontal"))

        self.btn_open_templates = QPushButton("Templates")
        self.btn_open_templates.setIcon(get_icon("folder.png"))
        self.btn_open_templates.setIconSize(QSize(30, 30))
        self.btn_open_templates.setMinimumHeight(45)
        self.btn_open_templates.setMinimumWidth(120)
        self.lay_buttons.addWidget(self.btn_open_templates)

        self.btn_clear = QPushButton("Limpar")
        self.btn_clear.setIcon(get_icon("clear.png"))
        self.btn_clear.setIconSize(QSize(40, 40))
        self.btn_clear.setMinimumHeight(45)
        self.btn_clear.setMinimumWidth(120)
        self.lay_buttons.addWidget(self.btn_clear)

        self.btn_open_writer = QPushButton("Abrir Writer")
        self.btn_open_writer.setIcon(get_icon("writer.png"))
        self.btn_open_writer.setIconSize(QSize(25, 25))
        self.btn_open_writer.setMinimumHeight(45)
        self.btn_open_writer.setMinimumWidth(120)
        self.lay_buttons.addWidget(self.btn_open_writer)

        self.btn_render_file = QPushButton("Renderizar arquivo")
        self.btn_render_file.setIcon(get_icon("file.png"))
        self.btn_render_file.setIconSize(QSize(30, 30))
        self.btn_render_file.setMinimumHeight(45)
        self.btn_render_file.setMinimumWidth(120)
        self.lay_buttons.addWidget(self.btn_render_file)

        self.btn_render_writer = QPushButton("Renderizar no Writer")
        self.btn_render_writer.setIcon(get_icon("paste.png"))
        self.btn_render_writer.setIconSize(QSize(25, 25))
        self.btn_render_writer.setMinimumHeight(45)
        self.btn_render_writer.setMinimumWidth(120)
        self.lay_buttons.addWidget(self.btn_render_writer)

        self.main_layout.addLayout(self.lay_buttons)

    def connections(self):
        self.cbx_form.currentTextChanged.connect(self.change_model)
        self.btn_render_file.clicked.connect(self.render_file)
        self.btn_render_writer.clicked.connect(self.render_to_writer)
        self.btn_open_templates.clicked.connect(self.open_templates)
        self.btn_clear.clicked.connect(self.clear_form)
        self.btn_open_writer.clicked.connect(open_writer)

    def clear_form(self):
        self.current_form.clear_content()

    def change_model(self, value):
        self.load_form(value)

    def choose_save_file(self) -> Path | None:
        file_dialog = QFileDialog()
        file_dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)
        file_dialog.setNameFilter("ODT Files (*.odt)")
        file_dialog.setDefaultSuffix("odt")
        file_dialog.setDirectory(str(Path(".").absolute()))
        if file_dialog.exec_():
            return Path(file_dialog.selectedFiles()[0])
        return None

    def render_file(self):
        context, errors = self.current_form.get_context()
        if errors:
            QMessageBox.warning(self, "Erro de formulário",
                                "Há erros em seu formulário. Corrija-os antes de prosseguir.")
            return
        repo.save_last_context_dev(context, False)
        context = self.current_form.pre_process(context)
        repo.save_last_context_dev(context, True)
        self.current_form.save_last_context()

        repo.save_last_context_dev(context, True)
        save_file = config.LOCAL_FOLDER / \
            "compiled.odt" if config.ENV == "dev" else self.choose_save_file()
        if save_file:
            renderer = Renderer(self.current_form.templates_dir)
            try:
                renderer.pre_render("main.odt", save_file,
                                    overwrite=True, **context)
                open_writer(save_file)
                QMessageBox.information(self, "Pós processamento",
                                        "Aguarde o documento terminar de ser aberto no Writer e clique em OK.")
                wh = WriterHandler()
                wh.run_macro("pos_process", str(
                    renderer.render_files.files_dir))
                self.close()
            except Exception as e:
                traceback.print_exc()
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
        repo.save_last_context_dev(context, False)
        context = self.current_form.pre_process(context)
        repo.save_last_context_dev(context, True)
        self.current_form.save_last_context()
        path = config.TEMPDIR / f"{uuid4().hex}.odt"
        renderer = Renderer(self.current_form.templates_dir)
        try:
            renderer.pre_render("main.odt", path, overwrite=True, **context)
            wh = WriterHandler()
            wh.run_macro("add_doc", str(path))
            wh.run_macro("pos_process", str(renderer.render_files.files_dir))
            self.close()
        except Exception as e:
            traceback.print_exc()
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
