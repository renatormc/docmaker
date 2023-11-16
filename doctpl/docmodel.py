from typing import Callable, Literal
from doctpl.gui.widgets.widget import WidgetMatrix
from doctpl.custom_types import ContextType, FormatType
from pathlib import Path


class DocModel:
    def __init__(self, name: str,
                 widgets: WidgetMatrix | None = None,
                 templates_folder: Path | str | None = None,
                 lists_folder: Path | str | None = None,
                 format: FormatType = 'docx',
                 main_template: str | None = None) -> None:
        self.name = name
        self._widgets = widgets
        self.filters: dict[str, Callable] = {}
        self.global_funcs: dict[str, Callable] = {}
        self._pre_process: Callable[[ContextType], ContextType] | None = None
        self._templates_folder: Path | None = Path(
            templates_folder) if templates_folder else None
        self._lists_folder: Path | None = Path(
            lists_folder) if lists_folder else None
        self.format: FormatType = format
        self._main_template = main_template

    @property
    def widgets(self) -> WidgetMatrix:
        if self._widgets is None:
            raise Exception("widgets was not set")
        return self._widgets

    @widgets.setter
    def widgets(self, value: WidgetMatrix) -> None:
        self._widgets = value

    @property
    def lists_folder(self) -> Path:
        if self._lists_folder is None:
            raise Exception("lists_folder was not set")
        return self._lists_folder

    @lists_folder.setter
    def lists_folder(self, value: Path | str) -> None:
        self._lists_folder = Path(value)

    @property
    def templates_folder(self) -> Path:
        if self._templates_folder is None:
            raise Exception("templates_folder was not set")
        return self._templates_folder

    @templates_folder.setter
    def templates_folder(self, value: Path | str) -> None:
        self._templates_folder = Path(value)

    @property
    def main_template(self) -> FormatType:
        if self._main_template:
            return self._main_template
        return "main.odt" if self.format == "odt" else "main.docx"
        
    @main_template.setter
    def main_template(self, value: str) -> None:
        self._main_template = value

    def filter(self, name: str):
        def decorator(f):
            self.filters[name] = f
            return f
        return decorator

    def global_func(self, name: str):
        def decorator(f):
            self.global_funcs[name] = f
            return f
        return decorator

    def pre_process(self):
        def decorator(f: Callable[[ContextType], ContextType]):
            self._pre_process = f
            return f
        return decorator

    def apply_pre_process(self, context: ContextType) -> ContextType:
        if self._pre_process is not None:
            return self._pre_process(context)
        return context
