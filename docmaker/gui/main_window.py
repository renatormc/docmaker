from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QComboBox, QMessageBox, QPushButton, QFileDialog, QScrollArea
from PySide6.QtCore import QSize, QRect
from docmaker.gui.form import Form
from pathlib import Path
from docmaker.doc_handler.odt_handler.writer_handler import WriterHandler
from docmaker.doc_handler.docx_handler.word_handler import WordHandler
from docmaker.doc_handler import get_handler
from docmaker.gui.helpers import spacer, get_icon
from docmaker.config import get_config
import traceback
import docmaker.repo as repo
from docmaker.custom_types import ContextType
from docmaker.docmodel import DocModel
from docmaker.helpers import  open_in_filemanager, open_file
from .context_dialog import ContextDialog
from uuid import uuid4
from docmaker.doc_handler.odt_handler.helpers import get_files_dir_path

class MainWindow(QMainWindow):
    def __init__(self, docmodels: list[DocModel]) -> None:
        self.docmodels = {m.name: m for m in docmodels}
        super(self.__class__, self).__init__()
        self.setup_ui()
        self.connections()
        self._current_form: Form | None = None
        self.load_last()

    @property
    def current_form(self) -> Form:
        if self._current_form is None:
            raise Exception("current_form was not set")
        return self._current_form
        
    @current_form.setter
    def current_form(self, value: Form) -> None:
        self._current_form = value


    def load_form(self, name: str, context: ContextType | None = None) -> None:
        if self._current_form is not None:
            self._current_form.deleteLater()
        self.current_form = Form(self.docmodels[name])
        if context:
            self.current_form.load(context)
        else:
            self.current_form.load_last_context()
        self.scr_form.setWidget(self.current_form)
        # self.lay_form.addWidget(self.current_form)
        self.cbx_form.setCurrentText(name)
        # if self.current_form.docmodel.format == "odt":
        #     self.btn_insert.setEnabled(True)
        # else:
        #     self.btn_insert.setEnabled(False)

    def load_last(self):
        last_context = repo.get_last_context()
        
        if last_context:
            try:
                docmodel = self.docmodels[last_context["model_name"]]
                self.load_form(docmodel.name, last_context["context"])
                return
            except KeyError:
                pass
        else:
            name = [name for name in self.docmodels.keys()][0]
            self.load_form(name)
        
    def setup_ui(self):
        self.setWindowIcon(get_icon("app_icon.png"))
        self.main_layout = QVBoxLayout()
        w = QWidget()
        w.setLayout(self.main_layout)
        self.setCentralWidget(w)

        self.cbx_form = QComboBox()
        for name in self.docmodels.keys():
            self.cbx_form.addItem(name)
        self.main_layout.addWidget(self.cbx_form)
        self.scr_form = QScrollArea(self)
        self.scr_form.setWidgetResizable(True)
        self.main_layout.addWidget(self.scr_form)

        self.create_buttons()
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

        self.btn_context = QPushButton("Gerar contexto")
        self.btn_context.setIcon(get_icon("json.png"))
        self.btn_context.setIconSize(QSize(25, 25))
        self.btn_context.setMinimumHeight(45)
        self.btn_context.setMinimumWidth(120)
        self.lay_buttons.addWidget(self.btn_context)

        self.btn_insert = QPushButton("Inserir")
        self.btn_insert.setIcon(get_icon("paste.png"))
        self.btn_insert.setIconSize(QSize(30, 30))
        self.btn_insert.setMinimumHeight(45)
        self.btn_insert.setMinimumWidth(120)
        self.lay_buttons.addWidget(self.btn_insert)

        self.btn_render_file = QPushButton("Renderizar arquivo")
        self.btn_render_file.setIcon(get_icon("file.png"))
        self.btn_render_file.setIconSize(QSize(30, 30))
        self.btn_render_file.setMinimumHeight(45)
        self.btn_render_file.setMinimumWidth(120)
        self.lay_buttons.addWidget(self.btn_render_file)

        self.main_layout.addLayout(self.lay_buttons)

    def connections(self):
        self.cbx_form.currentTextChanged.connect(self.change_model)
        self.btn_render_file.clicked.connect(self.render_file)
        self.btn_clear.clicked.connect(self.clear_form)
        self.btn_open_templates.clicked.connect(self.open_templates)
        self.btn_context.clicked.connect(self.show_context)
        self.btn_insert.clicked.connect(self.insert_on_editor)
  
    def clear_form(self):
        self.current_form.clear_content()

    def change_model(self, value):
        self.load_form(value)

    def choose_save_file(self) -> Path | None:
        file_dialog = QFileDialog()
        file_dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)
        file_dialog.setNameFilter("DOCX Files (*.docx)")
        file_dialog.setDefaultSuffix("docx")
        file_dialog.setDirectory(str(Path(".").absolute()))
        if file_dialog.exec_():
            return Path(file_dialog.selectedFiles()[0])
        return None
    
    def open_templates(self):
        open_in_filemanager(self.current_form.docmodel.templates_folder)

    def render_doc(self, save_file: Path) -> bool:
        context = self.gen_context()
        if context is None:
            return False
        if self.current_form is None:
            return False
        hd = get_handler(self.current_form.docmodel)
        try:
            hd.render(self.current_form.docmodel.main_template, context, save_file)
        except Exception as e:
            traceback.print_exc()
            QMessageBox.warning(self, "Erro", str(e))
            return False
        return True


    def render_file(self):
        save_file = self.current_form.docmodel.get_save_file() or self.choose_save_file()
        if save_file:
            res = self.render_doc(save_file)
            if res and get_config().open_file_after_render:
                open_file(save_file, self.current_form.docmodel.format)
                self.close()            
               

    def insert_on_editor(self):
        cf = get_config()
        save_file = cf.tempdir /  f"{uuid4().hex}.{self.current_form.docmodel.format}"
        res = self.render_doc(save_file)
        if res:
            if self.current_form.docmodel.format == "odt":
                wh = WriterHandler()
                wh.run_macro("add_doc", str(save_file))
                wh.run_macro("pos_process", files_dir=str(get_files_dir_path(save_file)))
            else:
                wh = WordHandler()
                wh.add_subdoc(save_file)
                        
            
    def gen_context(self) -> ContextType | None:
        context, errors = self.current_form.get_context()
        if errors:
            QMessageBox.warning(self, "Erro de formulário",
                                "Há erros em seu formulário. Corrija-os antes de prosseguir.")
            return None
        repo.save_last_context_dev(context, False)
        context = self.current_form.pre_process(context)
        repo.save_last_context_dev(context, True)
        self.current_form.save_last_context()
        return context
    
    def show_context(self):
        context = self.gen_context()
        if context is None:
            return
        dialog = ContextDialog(self, context)
        dialog.exec()

          


