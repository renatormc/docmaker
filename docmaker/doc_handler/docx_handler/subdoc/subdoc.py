from pathlib import Path
from typing import Any
from docxtpl.subdoc import Subdoc
from docxtpl import DocxTemplate
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from docmaker.doc_handler.docx_handler.docx_handler import DocxHandler

def add_subdoc_from_template(tpl: DocxTemplate, template: str|Path, context: Any) -> Subdoc:
    path = Path(template)
    if not path.exists():
        raise FileNotFoundError(f"the template \"{path}\" was not found")
    subtpl = DocxTemplate(str(path))
    subtpl.render(context)
    sd: Subdoc = tpl.new_subdoc()
    sd.subdocx = subtpl.docx
    return sd
       

class SubdocFunction:
    def __init__(self, tpl: DocxTemplate, handler: 'DocxHandler'):
        self.tpl = tpl
        self.handler = handler

    def __call__(self, template: str, **kargs):
        path = self.handler.docmodel.templates_folder / template
        if not path.exists():
            return ""
        try:
            return add_subdoc_from_template(self.tpl, path, kargs)
        except FileNotFoundError:
            return 
      