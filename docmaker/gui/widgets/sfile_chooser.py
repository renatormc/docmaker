from pathlib import Path
from typing import Any, Literal, Optional, TYPE_CHECKING
from docmaker.gui.widgets.helpers import apply_converter
from docmaker.gui.widgets.types import ValidationError

from PySide6.QtWidgets import QLineEdit
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QToolButton, QFileDialog
from docmaker.custom_types import ConverterType, ValidatorType
from docmaker.gui.widgets.label_error import LabelError
if TYPE_CHECKING:
    from docmaker.docmodel import DocModel


class SFileChooser:

    def __init__(
            self, name: str, required=False, label="",
            placeholder="", validators: list[ValidatorType] = [],
            stretch=0, default: str | Path = "", converter: Optional[ConverterType] = None, type: Literal['file', 'dir'] = 'file', default_dir=".") -> None:
        self.required = required
        self.placeholder = placeholder
        self._name = name
        self.validators = validators
        self._label = label or self.name
        self._stretch = stretch
        self.default = Path(default)
        self.converter = converter
        self.default_dir = default_dir
        self._docmodel: Optional[DocModel] = None
        self.type: Literal['file', 'dir'] = type
        super(SFileChooser, self).__init__()
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
        return self._name

    def set_docmodel(self, docmodel: 'DocModel') -> None:
        self._docmodel = docmodel

    def get_docmodel(self) -> 'DocModel':
        if self._docmodel is None:
            raise Exception("Docmodel was not set")
        return self._docmodel

    def get_context(self) -> Any:
        data = self.w.displayText().strip()
        if self.required and data == "":
            raise ValidationError('O valor não pode ser vazio')
        if data == "":
            return None
        path = Path(data)
        if not path.exists():
            raise ValidationError('Diretório ou arquivo não existente')
        if self.type == "dir" and not path.is_dir():
            raise ValidationError('Somente diretório é permitido')
        if self.type == "file" and not path.is_file():
            raise ValidationError('Somente arquivo é permitido')
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
        self._w = QLineEdit()
        self._w.setPlaceholderText(self.placeholder)
        lay_horizontal = QHBoxLayout()
        lay_horizontal.addWidget(self._w)

        btn = QToolButton()
        btn.setText("...")
        btn.clicked.connect(self.choose_dir)
        lay_horizontal.addWidget(btn)

        l.addLayout(lay_horizontal)
        self._lbl_error = LabelError()
        l.addWidget(self._lbl_error)
        return w

    def show_error(self, message: str) -> None:
        self.lbl_error.setText(message)

    def serialize(self) -> Any:
        return self.w.displayText()

    def load(self, value: Any) -> None:
        self.w.setText(value)

    def clear_content(self) -> None:
        self.w.setText(str(self.default))

    def choose_dir(self):
        if self.type == 'file':
            file_, ok = QFileDialog.getOpenFileName(
                self.w, "Escolher arquivo", self.default_dir)
            if ok:
                path = Path(file_)
                self.w.setText(str(path))
        elif self.type == 'dir':
            dir_ = QFileDialog.getExistingDirectory(
                self.w, "Escolher diretório", self.default_dir)
            if dir_:
                path = Path(dir_)
                self.w.setText(str(path))
