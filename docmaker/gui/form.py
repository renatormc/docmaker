from typing import Optional
from docmaker.gui.widgets.scomposite import SComposite
from PySide6.QtWidgets import QFileDialog
import json
from pathlib import Path
import docmaker.repo as repo
from docmaker.docmodel import DocModel
from docmaker.custom_types import ContextType
from docmaker.helpers import read_json_file, write_json_file

class Form(SComposite):

    def __init__(self, docmodel: DocModel):
        self.docmodel = docmodel
        self.docmodel.current_form = self
        super(Form, self).__init__(docmodel.widgets, docmodel=docmodel)

    def save_last_context(self):
        data = self.serialize()
        repo.save_last_context(self.docmodel.name,  data)

    def load_last_context(self):
        data = repo.get_last_context_by_model(self.docmodel.name)
        self.load(data)

    def save_to_file(self, file_: Optional[str] = None):
        data = self.serialize()
        file_ = file_ or QFileDialog.getSaveFileName(
            self, "Escolha o arquivo",  ".", "JSON (*.json)")[0]
        if file_:
            write_json_file(file_, data)
           

    def load_from_file(self, file_: Optional[str] = None) -> None:
        file_ = file_ or QFileDialog.getOpenFileName(
            self, "Escolha o arquivo",  ".", "JSON (*.json)")[0]
        if file_:
            path = Path(file_)
            if path.exists():
                data = read_json_file(file_)
                self.load(data)

    def pre_process(self, context: ContextType) -> ContextType:
        return self.docmodel.apply_pre_process(context)
       