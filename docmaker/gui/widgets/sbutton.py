from typing import Any, Optional, TYPE_CHECKING, Callable

from PySide6.QtWidgets import QLineEdit
from PySide6.QtWidgets import QWidget,  QPushButton
from docmaker.gui.widgets.label_error import LabelError
if TYPE_CHECKING:
    from docmaker.docmodel import DocModel

class SButton:

    def __init__(
            self, label: str,
            on_click: Callable,
            stretch=0) -> None:
        self.on_click = on_click
        self._label = label
        self._stretch = stretch
        self._docmodel: Optional[DocModel] = None 
        super(SButton, self).__init__()
        self._w: Optional[QLineEdit] = None
        self._lbl_error: Optional[LabelError] = None

    @property
    def stretch(self) -> int:
        return self._stretch

    @property
    def w(self) -> QLineEdit:
        if not self._w:
            raise Exception("get_widget must be executed once before")
        return self._w

    @property
    def lbl_error(self) -> LabelError:
        if not self._lbl_error:
            raise Exception("get_widget must be executed once before")
        return self._lbl_error

    @property
    def label(self) -> str:
        return self._label

    @property
    def name(self) -> str:
        return ""

    def set_docmodel(self, docmodel: 'DocModel') -> None:
        self._docmodel = docmodel

    def get_docmodel(self) -> 'DocModel':
        if self._docmodel is None:
            raise Exception("Docmodel was not set")
        return self._docmodel

    def get_context(self) -> Any:
        return None

    def get_widget(self) -> QWidget:
        w = QPushButton(self.label)
        w.clicked.connect(self.on_click)
        return w

    def show_error(self, message: str) -> None:
        pass

    def serialize(self) -> Any:
        return ""

    def load(self, value: Any) -> None:
        pass

    def clear_content(self) -> None:
        pass
