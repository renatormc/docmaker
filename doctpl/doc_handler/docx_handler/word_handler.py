import os
if os.name == "nt":
    import win32com.client
from pathlib import Path

class WordHandler:
    def __init__(self) -> None:
        self.word_app = win32com.client.Dispatch("Word.Application")
        self.active_doc = self.word_app.ActiveDocument

    def write_text(self, text: str) -> None:
        selection = self.word_app.Selection
        selection.TypeText(text)

    def add_subdoc(self, path: Path | str) -> None:
        selection = self.word_app.Selection
        selection.InsertFile(str(path))