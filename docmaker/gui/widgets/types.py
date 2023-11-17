from PySide6.QtCore import QSize
from pathlib import Path
from typing import TypedDict


class ValidationError(Exception):
    pass

class ObjectPicUserData:
    def __init__(self, pic: Path, original_size: QSize) -> None:
        self.pic = pic
        self.original_size = original_size
   