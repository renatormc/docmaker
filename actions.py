from pathlib import Path
import sys
import config
from doctpl.gui.form import BaseForm

def show_gui(directory: Path):
    from PySide6.QtWidgets import QApplication
    from doctpl.gui.main_window import MainWindow
    import models
    import logging

    path = Path.home() / ".rmc/log/doctpl.log"
    try:
        path.parent.mkdir(parents=True)
    except FileExistsError:
        pass
    logging.basicConfig(filename=str(
        path), encoding='utf-8', level=logging.DEBUG)
    app = QApplication(sys.argv)
    forms: list[BaseForm] = []
    for entry in (config.APPDIR / "models").iterdir():
        if entry.is_dir():
            try:
                Form: BaseForm = getattr(models, entry.name).form.Form
                Form.templates_dir = str(entry.absolute() / "templates")
                forms.append(Form)
            except AttributeError:
                pass
    w = MainWindow(forms, directory)
    w.show()
    sys.exit(app.exec())