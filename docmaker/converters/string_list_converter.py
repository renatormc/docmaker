from docmaker.gui.widgets.types import ValidationError
from typing import TYPE_CHECKING


class StringListConverter:
    def __init__(self, sep=",") -> None:
        self.sep = sep
    
    def __call__(self,  value: str) -> list[str]:
        if not value:
            return []
        return [p.strip() for p in value.split(self.sep)]