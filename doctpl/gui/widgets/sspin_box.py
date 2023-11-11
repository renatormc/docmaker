from typing import Any, Optional
from doctpl.gui.widgets.helpers import apply_converter
from doctpl.gui.widgets.types import ValidationError

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSpinBox
from doctpl.custom_types import ConverterType, ValidatorType
from doctpl.gui.widgets.label_error import LabelError


class SSpinBox:

    def __init__(
            self, name: str, required=False, label="", validators: list[ValidatorType] = [],
            stretch=0, default=0, converter: Optional[ConverterType] = None,
            min: Optional[int] = None, max: Optional[int] = None) -> None:
        self.required = required
        self._name = name
        self.validators = validators
        self._label = label or self.name
        self._stretch = stretch
        self.default = default
        self.converter = converter
        self.min = min
        self.max = max
        self._model_name: Optional[str] = None
        super(SSpinBox, self).__init__()
        self._w: Optional[QSpinBox] = None
        self._lbl_error: Optional[LabelError] = None

    @property
    def stretch(self) -> int:
        return self._stretch

    @property
    def w(self) -> QSpinBox:
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

    def set_model_name(self, model_name: str) -> None:
        self._model_name = model_name

    def get_model_name(self) -> str:
        if self._model_name is None:
            raise Exception("Model name was not set")
        return self._model_name

    def get_context(self) -> Any:
        data = self.w.value()
        if self.required and data == "":
            raise ValidationError('O valor não pode ser vazio')
        if self.converter is not None:
            data = apply_converter(data, self.converter)
        for v in self.validators:
            v(data)
        return data

    def get_widget(self) -> QWidget:
        w = QWidget()
        l = QVBoxLayout()
        l.setSpacing(0)
        w.setLayout(l)
        l.addWidget(QLabel(self.label))
        self._w = QSpinBox()
        if self.min:
            self._w.setMinimum(self.min)
        if self.max:
            self._w.setMaximum(self.max)
        l.addWidget(self._w)
        self._lbl_error = LabelError()
        l.addWidget(self._lbl_error)
        return w

    def show_error(self, message: str) -> None:
        self.lbl_error.setText(message)

    def serialize(self) -> Any:
        return self.w.value()

    def load(self, value: Any) -> None:
        self.w.setValue(value)

    def clear_content(self) -> None:
        self.w.setValue(self.default)
