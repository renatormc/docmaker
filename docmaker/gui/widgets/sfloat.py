from typing import Any, Optional, TYPE_CHECKING
from docmaker.gui.widgets.helpers import apply_converter
from docmaker.gui.widgets.types import ValidationError

from PySide6.QtWidgets import QLineEdit
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from docmaker.custom_types import ConverterType, ValidatorType
from docmaker.gui.widgets.label_error import LabelError
if TYPE_CHECKING:
    from docmaker.docmodel import DocModel

class SFloat:

    def __init__(
            self, name: str, required=False, label="",
            placeholder="", validators: list[ValidatorType] = [],
            stretch=0, default: Optional[float]=None, converter: Optional[ConverterType] = None) -> None:
        self.required = required
        self.placeholder = placeholder
        self._name = name
        self.validators = validators
        self._label = label or self.name
        self._stretch = stretch
        self.default: Optional[float] = default
        self.converter = converter
        self._docmodel: Optional[DocModel] = None 
        super(SFloat, self).__init__()
        self._w: Optional[QLineEdit] = None
        self._lbl_error: Optional[LabelError] = None

    @property
    def float_value(self) -> float:
        return float(self.w.displayText().replace(",", "."))

    @float_value.setter
    def float_value(self, value: float):
        self.w.setText(str(value).replace(".", ","))

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
        return self._name

    def set_docmodel(self, docmodel: 'DocModel') -> None:
        self._docmodel = docmodel

    def get_docmodel(self) -> 'DocModel':
        if self._docmodel is None:
            raise Exception("Docmodel was not set")
        return self._docmodel

    def get_context(self) -> Any:
        text = self.w.displayText().strip()
        if self.required and text == "":
            raise ValidationError('O valor não pode ser vazio')
        if text == "":
            return None
        try:
            data = self.float_value
        except:
            raise ValidationError('Valor incorreto')
        if self.converter is not None:
            data =  apply_converter(data, self.converter)
        for v in self.validators:
            v(data)
        return data

    def get_widget(self) -> QWidget:
        w = QWidget()
        l = QVBoxLayout()
        l.setSpacing(0)
        w.setLayout(l)
        l.addWidget(QLabel(self.label))
        self._w = QLineEdit()
        self._w.setPlaceholderText(self.placeholder)
        l.addWidget(self._w)
        self._lbl_error = LabelError()
        l.addWidget(self._lbl_error)
        return w

    def show_error(self, message: str) -> None:
        self.lbl_error.setText(message)

    def serialize(self) -> Any:
        try:
            return self.float_value
        except:
            return None
       

    def load(self, value: Any) -> None:
        try:
            self.float_value = value
        except:
            self.w.setText("")
       

    def clear_content(self) -> None:
        try:
            if self.default is not None:
                self.float_value = self.default
            else:
                self.w.setText("")
        except:
            self.w.setText("")
