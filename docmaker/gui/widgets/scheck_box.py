from typing import Any, Optional, TYPE_CHECKING
from docmaker.gui.widgets.helpers import apply_converter

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QCheckBox
from docmaker.custom_types import ConverterType
from docmaker.gui.widgets.label_error import LabelError
if TYPE_CHECKING:
    from docmaker.docmodel import DocModel


class SCheckBox:

    def __init__(self, name: str, label="", stretch=0, default=False, converter: Optional[ConverterType] = None) -> None:
        self._name = name
        self._label = label or self.name
        self._stretch = stretch
        self.default = default
        self.converter = converter
        self._docmodel: Optional[DocModel] = None 
        super(SCheckBox, self).__init__()
        self._w: Optional[QCheckBox] = None
        self._lbl_error: Optional[LabelError] = None

    @property
    def stretch(self) -> int:
        return self._stretch

    @property
    def w(self) -> QCheckBox:
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
        return self._name

    def set_docmodel(self, docmodel: 'DocModel') -> None:
        self._docmodel = docmodel

    def get_docmodel(self) -> 'DocModel':
        if self._docmodel is None:
            raise Exception("Docmodel was not set")
        return self._docmodel
    
    
    def get_context(self) -> Any:
        data = self.w.isChecked()
        if self.converter is not None:
            data =  apply_converter(data, self.converter)
        return data

    def get_widget(self) -> QWidget:
        w = QWidget()
        l = QVBoxLayout()
        l.setSpacing(0)
        w.setLayout(l)
        l.addWidget(QLabel())
        self._w = QCheckBox()
        self._w.setText(self.label)
        l.addWidget(self._w)
        self._lbl_error = LabelError()
        l.addWidget(self._lbl_error)
        return w

    def show_error(self, message: str) -> None:
        self.lbl_error.setText(message)

    def serialize(self) -> Any:
        return self.w.isChecked()

    def load(self, value: Any) -> None:
        self.w.setChecked(value)

    def clear_content(self) -> None:
        self.w.setChecked(self.default)
