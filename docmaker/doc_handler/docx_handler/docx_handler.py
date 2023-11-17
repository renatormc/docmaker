from pathlib import Path
from typing import Optional, Union
from docxtpl import DocxTemplate, InlineImage, Subdoc
from docmaker.doc_handler.docx_handler.jenv import make_jinja_env
from docx.shared import Mm
from docmaker.doc_handler.docx_handler.subdoc_html import SubdocHtmlFunction
from docmaker.doc_handler.docx_handler.subdoc import SubdocFunction
from docmaker.docmodel import DocModel
from docmaker.custom_types import ContextType

class SInlineImage:
    def __init__(self, tpl):
        self.tpl = tpl

    def __call__(self, file, width):
        path = Path(file)
        if not path.exists():
            return
        return InlineImage(self.tpl, file, width=Mm(width))


class DocxHandler:
    def __init__(self, docmodel: DocModel):
        self.docmodel = docmodel
        self.jinja_env = make_jinja_env(docmodel.filters, docmodel.global_funcs, docmodel.templates_folder)
        self.context: ContextType | None = None
        self.pos_subdocs: list[Subdoc]  = []

    def prepare_jinja_env(self, tpl: DocxTemplate):
        self.jinja_env.globals['subdoc'] = SubdocFunction(tpl, self)
        jinja_env2 = make_jinja_env(self.docmodel.filters, self.docmodel.global_funcs, self.docmodel.templates_folder)
        self.jinja_env.globals['subdoc_html'] = SubdocHtmlFunction(self, tpl, jinja_env2)
        self.jinja_env.globals['image'] = SInlineImage(tpl)
        return self.jinja_env


    def render(self, template: str, context: ContextType, dest_file: Union[Path, str]) -> Optional[Path]:
        self.context = context
        dest_file = Path(dest_file)
        path = self.docmodel.templates_folder / template
        if path.exists():
            tpl = DocxTemplate(str(path))
            jinja_env = self.prepare_jinja_env(tpl)
            tpl.render(context, jinja_env)
            tpl.save(dest_file)
            return dest_file
        return None
