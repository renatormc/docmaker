from typing import Any, TYPE_CHECKING
from bs4 import BeautifulSoup
from docxtpl import DocxTemplate, Subdoc
import jinja2
from .elment_parses import parse_element


if TYPE_CHECKING:
    from docmaker.doc_handler.docx_handler import DocxHandler


class SubdocDocxFunction:
    def __init__(self, docx_handler: 'DocxHandler', tpl: DocxTemplate) -> None:
       self.docx_handler = docx_handler
       self.tpl = tpl

    def __call__(self, template, **context):
        n = len(self.docx_handler.pos_subdocs)
        path = self.docx_handler.docmodel.templates_folder / template
        subtpl = DocxTemplate(path)
        subtpl.render(context)
        self.docx_handler.pos_subdocs.append(subtpl)
        return "{{p " + f"pos_subdocs[{n}]" + " }}"


class SubdocHtmlFunction:
    def __init__(self, docx_handler: 'DocxHandler', tpl: DocxTemplate, jinja_env: jinja2.Environment):
        self.tpl = tpl
        self.jinja_env = jinja_env
        self.jinja_env.globals['subdoc_docx'] = SubdocDocxFunction(docx_handler, tpl)
        self.docx_handler = docx_handler


    def __call__(self, template: str, context: Any = None) -> Subdoc:
        if not isinstance(context, dict):
            context = {'data': context}
        sd = self.tpl.new_subdoc()
        path = self.docx_handler.docmodel.templates_folder / template
        if not path.exists():
            raise FileNotFoundError(f"the template \"{path}\" was not found")
        tp = self.jinja_env.get_template(template)
        text = tp.render(ctx=self.docx_handler.context, **context)
        soup = BeautifulSoup(text, 'html.parser')
        for e in soup.find_all(recursive=False):
            parse_element(sd, e)
        return sd
