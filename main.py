import argparse
from pathlib import Path
import config
import sys
import os
import stat
from doctpl.helpers import add_to_path
import json

def link_macro():
    folder = Path.home()
    aux = "Libreoffice" if os.name == "nt" else "libreoffice"
    for item in folder.glob(f"**/{aux}/**/Scripts/**/python"):
        if item.is_dir():
            pfrom = config.APPDIR / "doctpl/macros/doctpl.py"
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
            rmc_folder = Path.home() / ".rmc"
            for d in [rmc_folder / "bin", rmc_folder / "etc"]:
                try:
                    d.mkdir(parents=True)
                except FileExistsError:
                    pass
            lines = [
                f"{sys.executable} {config.APPDIR / 'main.py'} %*"
            ]
            bin_folder = rmc_folder / "bin"
            add_to_path(bin_folder)
            path = bin_folder / "doctpl.bat"
            text = "\n".join(lines)
            path.write_text(text)
            with (rmc_folder / "etc/doctpl.json").open("w") as f:
                f.write(json.dumps({"python_interpreter": sys.executable}))
            link_macro()
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
        from models import forms
        app = QApplication(sys.argv)
        w = MainWindow(forms, args.dir)
        w.show()
        sys.exit(app.exec())
   