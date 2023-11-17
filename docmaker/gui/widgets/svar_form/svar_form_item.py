from typing import Optional
from docmaker.gui.widgets.scomposite import SComposite
from docmaker.gui.widgets.widget import Widget
import copy


class SVarFormItem:
    def __init__(self, choice_value: str, widgets: list[list[Widget]]) -> None:
        self.choice_value = choice_value
        self.widgets = widgets
        self._composite: Optional[SComposite] = None

    @property
    def composite(self) -> SComposite:
        if self._composite is None:
            raise Exception("Composite was not initialized")
        return self._composite

    @composite.setter
    def composite(self, value: SComposite) -> None:
        self._composite = value
        self.composite.setStyleSheet("QWidget{background-color: white; padding-left: 0;}")

    def clone(self):
        widgets = copy.deepcopy(self.widgets)
        return SVarFormItem(self.choice_value, widgets)
        