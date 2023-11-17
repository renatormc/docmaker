from typing import  Optional, Tuple, TYPE_CHECKING
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QSpacerItem, QSizePolicy, QToolButton, QLabel
from PySide6.QtCore import Signal
from docmaker.custom_types import FormError
from docmaker.gui.widgets.widget import Widget
from docmaker.gui.widgets.types import ValidationError
from docmaker.gui.helpers import get_icon
if TYPE_CHECKING:
    from docmaker.docmodel import DocModel

class SComposite(QWidget):
    removeRequested = Signal(int)
    cloneRequested = Signal(int)

    def __init__(self, widgets: list[list[Widget]],
            color: Optional[str] = None, is_array_child=False, index: int = 0, docmodel: Optional['DocModel'] = None) -> None:
        super().__init__()
        self._index = index
        self.color = color
        self.widgets = widgets
        self._docmodel: Optional[DocModel] = docmodel
        self.widgets_map: dict[str, Widget] = {}
        for row in self.widgets:
            for item in row:
                self.widgets_map[item.name] = item
        self.is_array_child = is_array_child
        self.lbl_index: Optional[QLabel] = None
        self.setup_ui()

    @property
    def index(self) -> int:
        return self._index

    @index.setter
    def index(self, value: int) -> None:
        self._index = value
        if self.lbl_index is not None:
            self.lbl_index.setText(str(value + 1))

    def set_docmodel(self, docmodel: 'DocModel') -> None:
        self._docmodel = docmodel

    def get_docmodel(self) -> 'DocModel':
        if self._docmodel is None:
            raise Exception("Docmodel was not set")
        return self._docmodel

    def setup_ui(self):
        self.lay_main = QVBoxLayout()
        self.lay_main.setContentsMargins(0,0,0,0)
        self.lay_main.setSpacing(0)
        self.setLayout(self.lay_main)

        if self.is_array_child:
            lay = QHBoxLayout()
            lay.setContentsMargins(0,0,0,0)
            lay.setSpacing(2)
            self.lbl_index = QLabel(str(self.index + 1))
            self.lbl_index.setContentsMargins(10,0,0,0)
            lay.addWidget(self.lbl_index)
            # lay.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
            
            btn = QToolButton()
            btn.clicked.connect(self.request_clone)
            btn.setIcon(get_icon("clone.jpeg"))
            btn.setToolTip("Clonar")
            lay.addWidget(btn)

            btn = QToolButton()
            btn.clicked.connect(self.request_remove)
            btn.setIcon(get_icon("x.png"))
            btn.setToolTip("Remover")
            lay.addWidget(btn)
    
            self.lay_main.addLayout(lay)

        for row in self.widgets:
            h_layout = QHBoxLayout()
            self.lay_main.addLayout(h_layout)
            for i, item in enumerate(row):
                item.set_docmodel(self.get_docmodel())
                w = item.get_widget()
                h_layout.addWidget(w)
                h_layout.setStretch(i, item.stretch)
        spacer_item = QSpacerItem(40, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.lay_main.addSpacerItem(spacer_item)
        if self.color:
            self.setStyleSheet(f"background-color: {self.color}; border-color: {self.color};")
        
    def get_field_value(self, field: str):
        try:
            w = self.widgets_map[field]
            return w.get_context()
        except KeyError:
            return None

    def get_context(self) -> Tuple[dict, FormError]:
        context = {}
        errors: FormError = {}
        for row in self.widgets:
            for item in row:
                if not item.name:
                    continue
                message = ""
                try:
                    context[item.name] = item.get_context()
                except ValidationError as e:
                    message = str(e)
                    errors[item.name] = message
                item.show_error(message)
        return context, errors

    def load(self, data: dict) -> None:
        for key, w in self.widgets_map.items():
            try:
                w.load(data[key])
            except Exception:
                pass

    def serialize(self):
        data = {}
        for row in self.widgets:
            for item in row:
                data[item.name] = item.serialize()
        return data

    def clear_content(self):
        for row in self.widgets:
            for item in row:
                item.clear_content()

    def request_remove(self):
        self.removeRequested.emit(self.index)

    def request_clone(self):
        self.cloneRequested.emit(self.index)
