from docmaker.config import LIBDIR
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QMessageBox, QWidget, QSpacerItem, QSizePolicy
from typing import Literal

def get_icon(name):
    return QIcon(str(LIBDIR / "gui/assets/images" / name)) 


def ask_confirmation(parent: QWidget, title: str, message: str) -> bool:
    msg_box = QMessageBox(parent)
    msg_box.setIcon(QMessageBox.Icon.Question)
    msg_box.setWindowIcon(parent.windowIcon())
    msg_box.setText(message)
    msg_box.setWindowTitle(title)
    btn_yes = msg_box.addButton(QMessageBox.StandardButton.Yes)
    btn_no = msg_box.addButton(QMessageBox.StandardButton.No)
    msg_box.setDefaultButton(btn_no)
    btn_yes.setText("Sim")
    btn_no.setText("Não")
    msg_box.exec_()
    if msg_box.clickedButton() == btn_yes:
        return True
    return False

def spacer(direction: Literal["horizontal", "vertical"]) -> QSpacerItem:
    if direction == "horizontal":
        return QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
    return QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

