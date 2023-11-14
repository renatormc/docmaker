from typing import Callable
from doctpl.gui.widgets.widget import WidgetMatrix
from doctpl.custom_types import ContextType
from pathlib import Path


class DocModel:
    def __init__(self, name: str, widgets: WidgetMatrix | None = None, templates_folder: Path | str | None = None) -> None:
        self.name = name
        self._widgets = widgets
        self.filters: dict[str, Callable] = {}
        self.global_funcs: dict[str, Callable] = {}
        self._pre_process: Callable[[ContextType], ContextType] | None = None
        self._templates_dir: Path | None = Path(templates_folder) if templates_folder else None

    @property
    def widgets(self) -> WidgetMatrix:
        if self._widgets is None:
            raise Exception("widgets was not set")
        return self._widgets

    @widgets.setter
    def widgets(self, value: WidgetMatrix) -> None:
        self._widgets = value

    @property
    def templates_dir(self) -> Path:
        if self._templates_dir is None:
            raise Exception("templates_folder was not set")
        return self._templates_dir

    @templates_dir.setter
    def templates_dir(self, value: Path | str) -> None:
        self._templates_dir = Path(value)

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

    def pre_process(self, context: ContextType):
        def decorator(f: Callable[[ContextType], ContextType]):
            self._pre_process = f
            return f
        return decorator
