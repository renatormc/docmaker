from typing import Any, Optional, TYPE_CHECKING
from docmaker.gui.widgets.scomposite import SComposite
from docmaker.gui.widgets.widget import Widget
from docmaker.gui.widgets.types import ValidationError
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSpinBox, QPushButton, QSpacerItem, QSizePolicy
from PySide6.QtCore import QSize
from docmaker.gui.helpers import get_icon
from docmaker.gui.colors import Colors
import copy
if TYPE_CHECKING:
    from docmaker.docmodel import DocModel


class SArray:
    def __init__(self, name: str, widgets: list[list[Widget]], label="", stretch=0, model_name: Optional[str] = None) -> None:
        self._name = name
        self._label = label or self.name
        self._stretch = stretch
        self.widgets = widgets
        self._model_name = model_name
        super(SArray, self).__init__()
        self._composites: Optional[list[SComposite]] = None

    @property
    def stretch(self) -> int:
        return self._stretch

    @property
    def composites(self) -> list[SComposite]:
        if self._composites is None:
            raise Exception("get_widget must be executed once before")
        return self._composites

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

    def show_total_items(self):
        self.lbl_total_items.setText(f"Total: {len(self.composites)}")

    def get_context(self) -> Any:
        data = []
        errors = False
        for comp in self.composites:
            c, error = comp.get_context()
            if error:
                errors = True
            data.append(c)
        if errors:
            raise ValidationError("Há erros")
        return data

    def get_widget(self) -> QWidget:
        w = QWidget()
        w.setStyleSheet(f"background-color: {Colors.array_widget_background};")
        w.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        lay_main = QVBoxLayout()
        # lay_main.setContentsMargins(0,0,0,0)
        # lay_main.setSpacing(0)
        w.setLayout(lay_main)

        lay_main.addWidget(QLabel(self.label))

        lay_horizontal = QHBoxLayout()

        self.spb_add = QSpinBox()
        self.spb_add.setMinimumHeight(35)
        self.spb_add.setMinimum(1)
        lay_horizontal.addWidget(self.spb_add)

        self.btn_add = QPushButton("Adicionar")
        self.btn_add.setMinimumHeight(35)
        self.btn_add.setIcon(get_icon("add.png"))
        self.btn_add.setIconSize(QSize(30,30))
        self.btn_add.clicked.connect(self.add_items)
        lay_horizontal.addWidget(self.btn_add)

        self.btn_remove_all = QPushButton("Remover todos")
        self.btn_remove_all.setMinimumHeight(35)
        self.btn_remove_all.setIcon(get_icon("x.png"))
        self.btn_remove_all.clicked.connect(self.remove_all_items)
        lay_horizontal.addWidget(self.btn_remove_all)
        lay_horizontal.setSpacing(2)

        lay_horizontal.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.lbl_total_items = QLabel("Total: 0")
        lay_horizontal.addWidget(self.lbl_total_items)
        
        lay_main.addLayout(lay_horizontal)

        

        self.lay_composites = QVBoxLayout()
        self.lay_composites.setContentsMargins(0,0,0,0)
        self.lay_composites.setSpacing(0)
        lay_main.addLayout(self.lay_composites)

        self._composites = []
        return w

    def add_items(self, qtd: Optional[int] = None):
        qtd = qtd or self.spb_add.value()
        n = len(self.composites)
        for i in range(qtd):
            index = n + i
            widgets = copy.deepcopy(self.widgets)
            # composite = SComposite(widgets, color=Colors.item_array_widget_background, is_array_child=True, index=index)
            composite = SComposite(widgets, is_array_child=True, index=index, color="white", docmodel=self.get_docmodel())
            composite.removeRequested.connect(self.remove_by_index)
            composite.cloneRequested.connect(self.clone_by_index)
            self.lay_composites.addWidget(composite)
            self.composites.append(composite)
        self.show_total_items()

    def remove_all_items(self):
        n = len(self.composites)
        for i in range(n):
            ri = n-i-1
            self.composites[ri].deleteLater()
            self.composites.pop(ri)
        self.show_total_items()
       
    def remove_by_index(self, index: int) -> None:
        self.composites[index].deleteLater()
        self.composites.pop(index)
        for i in range(index, len(self.composites)):
            self.composites[i].index -= 1
        self.show_total_items()

    def clone_by_index(self, index: int) -> None:
        data = self.composites[index].serialize()
        self.add_items(1)
        self.composites[-1].load(data)
       

    def serialize(self) -> Any:
        data = []
        for composite in self.composites:
            data.append(composite.serialize())
        return data

    def load(self, data: list[Any]) -> None:
        n = len(data)
        self.clear_content()
        self.add_items(n)
        for i in range(n):
            self.composites[i].load(data[i])


    def clear_content(self) -> None:
        self.remove_all_items()
        # for composite in self.composites:
        #     composite.clear_content()

    def show_error(self, message: str) -> None:
        pass


