import argparse
from pathlib import Path
from doctpl import config
import sys
import os
import stat

def link_macro():
    folder = Path.home()
    for item in folder.glob("**/libreoffice/**/Scripts/**/python"):
        if item.is_dir():
            pfrom = config.LIBDIR / "macros/doctpl.py"
            pto = item / "doctpl.py"
            try:
                pto.unlink()
            except FileNotFoundError:
                pass
            pto.symlink_to(pfrom)
            print(f"Link \"{pto}\" was created.")
            break
    else:
        print("Libreoffice scripts folder not found")

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(dest="command", required=True, help='Command to be used')

p_link_macro = subparsers.add_parser("link-macro")

p_install = subparsers.add_parser("install")

p_gui = subparsers.add_parser("gui")
p_gui.add_argument("-d", "--dir", required=True, help="Directory to generate pre compiled files")

args = parser.parse_args()
match args.command:
    case "link-macro":
        link_macro()
    case "install":
        if os.name == "nt":
            raise Exception("Not implemented for Windows yet")
        else:
            lines = [
                "#!/bin/bash",
                f"{sys.executable} -m doctpl $@"
            ]
            text = "\n".join(lines)
            folder = Path.home() / ".local/bin"
            try:
                folder.mkdir(parents=True)
            except FileExistsError:
                pass
            path = folder / "doctpl"
            path.write_text(text)
            st = path.stat()
            path.chmod(st.st_mode | stat.S_IEXEC)
            link_macro()
            
    case "gui":
        from PySide6.QtWidgets import QApplication
        from doctpl.gui.main_window import MainWindow
        # from models.celular.form import Form
        from doctpl.helpers import inspect_models_folder
        forms = inspect_models_folder(config.MODELS_DIR)
        app = QApplication(sys.argv)
        w = MainWindow(forms, args.dir)
        w.show()
        sys.exit(app.exec())
   