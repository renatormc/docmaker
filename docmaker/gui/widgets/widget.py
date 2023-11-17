from typing import Any, Protocol, TYPE_CHECKING
from PySide6.QtWidgets import QWidget
if TYPE_CHECKING:
    from docmaker.docmodel import DocModel

WidgetMatrix = list[list['Widget']]


class Widget(Protocol):

    def get_context(self) -> Any:
        ...

    def get_widget(self) -> QWidget:
        ...

    def show_error(self, message: str) -> None:
        ...

    def serialize(self) -> Any:
        ...

    def load(self, value: Any) -> None:
        ...

    def clear_content(self) -> None:
        ...

    def set_docmodel(self, docmodel: 'DocModel') -> None:
        ...

    def get_docmodel(self) -> 'DocModel':
        ...

    @property
    def name(self) -> str:
        ...

    @property
    def label(self) -> str:
        ...

    @property
    def stretch(self) -> int:
        ...

