from typing import TYPE_CHECKING, Protocol, Union, Optional
from pathlib import Path
from doctpl.doc_handler.docx_handler import DocxHandler
from doctpl.doc_handler.odt_handler import OdtHandler
from doctpl.custom_types import ContextType
if TYPE_CHECKING:
    from doctpl.docmodel import DocModel

class DocHandler(Protocol):

    def render(self, template: str, context: ContextType, dest_file: Union[Path, str]) -> Optional[Path]:
        ...

def get_handler(docmodel: 'DocModel') -> DocHandler:
    if docmodel.format == "docx":
        return DocxHandler(docmodel)
    elif docmodel.format == "odt":
        return OdtHandler(docmodel)