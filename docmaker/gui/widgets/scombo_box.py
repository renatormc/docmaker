from typing import Any, Optional, TYPE_CHECKING
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox
from docmaker.custom_types import ConverterType
from docmaker.gui.widgets.helpers import apply_converter
from docmaker.gui.widgets.label_error import LabelError
from docmaker.gui.widgets.helpers import get_list
if TYPE_CHECKING:
    from docmaker.docmodel import DocModel


class SComboBox:

    def __init__(self, name: str, label="", choices: list[str]|str=[], stretch=0, default="", converter: Optional[ConverterType] = None):
        self._name = name
        self.choices = choices
        self._label = label or self.name
        self._stretch = stretch
        self.default = default
        self.converter = converter
        super(SComboBox, self).__init__()
        self._combo: Optional[QComboBox] = None
        self._lbl_error: Optional[LabelError] = None
        self._docmodel: Optional[DocModel] = None 

    @property
    def stretch(self) -> int:
        return self._stretch

    @property
    def combo(self) -> QComboBox:
        if self._combo is None:
            raise Exception("get_widget must be executed once before")
        return self._combo

    @property
    def lbl_error(self) -> LabelError:
        if not self._lbl_error:
            raise Exception("get_widget must be executed once before")
        return self._lbl_error

    @property
    def name(self) -> str:
        return self._name

    @property
    def label(self) -> str:
        return self._label

    def set_docmodel(self, docmodel: 'DocModel') -> None:
        self._docmodel = docmodel

    def get_docmodel(self) -> 'DocModel':
        if self._docmodel is None:
            raise Exception("Docmodel was not set")
        return self._docmodel

    def get_context(self) -> Any:
        data = self.combo.currentData()
        if self.converter is not None:
            data = apply_converter(data, self.converter)
        return data

    def get_widget(self) -> QWidget:
        w = QWidget()
        l = QVBoxLayout()
        w.setLayout(l)
        l.addWidget(QLabel(self.label))
        self._combo = QComboBox()
        for item in get_list(self.choices, self.get_docmodel().lists_folder):
            self.combo.addItem(item["key"], item["data"])
        l.addWidget(self.combo)
        self._lbl_error = LabelError()
        l.addWidget(self._lbl_error)
        return w


    def show_error(self, message: str) -> None:
        self.lbl_error.setText(message)

    def serialize(self) -> Any:
        return self.get_context()

    def load(self, value: Any) -> None:
        self.combo.setCurrentText(value)

    def clear_content(self)-> None:
        if self.default != "":
            self.combo.setCurrentText(self.default)
