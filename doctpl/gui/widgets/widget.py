from typing import Any, Protocol
from PySide6.QtWidgets import QWidget

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

    def set_model_name(self, model_name: str) -> None:
        ...

    def get_model_name(self) -> str:
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

