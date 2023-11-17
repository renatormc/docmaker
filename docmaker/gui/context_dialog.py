from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton
from PySide6.QtGui import QTextDocument, QSyntaxHighlighter, QTextCharFormat, QFont, QColor
from docmaker.custom_types import ContextType
from docmaker.gui.helpers import spacer
import json
from typing import TYPE_CHECKING
import re
if TYPE_CHECKING:
    from .main_window import MainWindow


class JsonHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super(JsonHighlighter, self).__init__(parent)

        self.json_format = QTextCharFormat()
        self.json_format.setForeground(QColor('darkBlue'))
        self.json_format.setFontWeight(QFont.Weight.Bold)

        self.json_pattern = re.compile(r'"([^"]*)"\s*:')  # Regular expression to match JSON keys

    def highlightBlock(self, text):
        for match in self.json_pattern.finditer(text):
            start, end = match.start(1), match.end(1)
            self.setFormat(start, end - start, self.json_format)


class JsonHighlighterTextEdit(QTextEdit):
    def __init__(self, parent=None):
        super(JsonHighlighterTextEdit, self).__init__(parent)
        self.highlighter = JsonHighlighter(self.document())

class ContextDialog(QDialog):

    def __init__(self, parent: 'MainWindow', context: ContextType) -> None:
        self.context = context
        super(self.__class__, self).__init__(parent)
        self.lay_main = QVBoxLayout()
        self.setLayout(self.lay_main)
        self.resize(1000, 800)
        self.setWindowTitle("Contexto")
        
        self.txe_context = JsonHighlighterTextEdit()
        self.txe_context.setReadOnly(True)
        self.txe_context.setText(json.dumps(self.context, indent=4, ensure_ascii=False, default=str))
        self.lay_main.addWidget(self.txe_context)

        self.lay_buttons = QHBoxLayout()
        self.lay_buttons.addSpacerItem(spacer("horizontal"))
        self.btn_ok = QPushButton("OK")
        self.lay_buttons.addWidget(self.btn_ok)
        self.btn_ok.clicked.connect(self.close)
