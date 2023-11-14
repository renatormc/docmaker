from pathlib import Path
import sys
import config
from doctpl.gui.form import Form

def show_gui():
    from PySide6.QtWidgets import QApplication
    from doctpl.gui.main_window import MainWindow
    import models

    app = QApplication(sys.argv)
    forms: list[Form] = []
    for entry in (config.APPDIR / "models").iterdir():
        if entry.is_dir():
            try:
                Form: Form = getattr(models, entry.name).form.Form
                Form.templates_dir = str(entry.absolute() / "templates")
                forms.append(Form)
            except AttributeError:
                pass
    w = MainWindow(forms)
    w.show()
    sys.exit(app.exec())