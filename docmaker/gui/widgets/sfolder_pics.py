from pathlib import Path
from typing import Any, Optional, TYPE_CHECKING
from docmaker.gui.widgets.helpers import apply_converter
from docmaker.gui.widgets.types import ValidationError

from PySide6.QtWidgets import QLineEdit
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QToolButton, QFileDialog
from docmaker.custom_types import ConverterType, ValidatorType
from docmaker.gui.widgets.label_error import LabelError
if TYPE_CHECKING:
    from docmaker.docmodel import DocModel


class SFolderPics:

    def __init__(
            self, name: str, required=False, label="", placeholder="", validators: list[ValidatorType] = [],
            subfolders=False, extensions=[".jpg", ".png"], stretch=0, default="", converter: Optional[ConverterType] = None) -> None:
        self.required = required
        self.placeholder = placeholder
        self._name = name
        self.validators = validators
        self._label = label or self.name
        self.subfolders = subfolders
        self.extensions = extensions
        self._stretch = stretch
        self.default = default
        self.converter = converter
        self._docmodel: Optional[DocModel] = None 
        super(SFolderPics, self).__init__()
        self._led: Optional[QLineEdit] = None
        self._lbl_error: Optional[LabelError] = None
        self._btn_choose: Optional[QToolButton] = None

    @property
    def stretch(self) -> int:
        return self._stretch

    @property
    def led(self) -> QLineEdit:
        if not self._led:
            raise Exception("get_widget must be executed once before")
        return self._led

    @property
    def lbl_error(self) -> LabelError:
        if not self._lbl_error:
            raise Exception("get_widget must be executed once before")
        return self._lbl_error

    @property
    def btn_choose(self) -> QToolButton:
        if not self._btn_choose:
            raise Exception("get_widget must be executed once before")
        return self._btn_choose

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
        text = self.led.displayText().strip()
        path = Path(text)
        if self.required and text == "":
            raise ValidationError('O valor não pode ser vazio')
        if not path.exists():
            raise ValidationError('Pasta não existente')
        if self.subfolders:
            pics = []
            for sub in path.iterdir():
                if sub.is_dir():
                    pics.append({
                        "folder": sub.name,
                        "pics": [str(entry.absolute()) for entry in sub.iterdir() if entry.is_file() and entry.suffix.lower() in self.extensions]
                    }) 
            data: Any = pics
        else:
            data = [str(entry.absolute()) for entry in path.iterdir() if entry.is_file() and entry.suffix.lower() in self.extensions]
        if self.converter is not None:
            data = apply_converter(data, self.converter)
        for v in self.validators:
            v(data)
        return data


    def get_widget(self) -> QWidget:
        w = QWidget()
        l = QVBoxLayout()
        w.setLayout(l)
        l.addWidget(QLabel(self.label))
        l.setSpacing(0)
        h_layout = QHBoxLayout()
        self._led = QLineEdit()
        self._led.setPlaceholderText(self.placeholder)
        h_layout.addWidget(self._led)
        self._btn_choose = QToolButton()
        self._btn_choose.setText("...")
        self._btn_choose.clicked.connect(self.choose_folder)
        h_layout.addWidget(self._btn_choose)
        l.addLayout(h_layout)

        self._lbl_error = LabelError()
        l.addWidget(self._lbl_error)
        return w


    def show_error(self, message: str) -> None:
        self.lbl_error.setText(message)

    def choose_folder(self):
        dir_ = QFileDialog.getExistingDirectory(None, "Escolha um diretório", ".")
        if dir_:
            self.led.setText(dir_)

    def serialize(self) -> Any:
        return self.led.displayText()

    def load(self, value: Any) -> None:
        self.led.setText(value)

    def clear_content(self)-> None:
        self.led.setText(self.default)
