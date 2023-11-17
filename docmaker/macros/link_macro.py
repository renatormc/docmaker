from pathlib import Path
from docmaker.config import LIBDIR
import os

def link_lo_macro():
    folder = Path.home()
    aux = "Libreoffice" if os.name == "nt" else "libreoffice"
    for item in folder.glob(f"**/{aux}/**/Scripts/**/python"):
        if item.is_dir():
            pfrom = LIBDIR / "macros/docmaker.py"
            pto = item / "docmaker.py"
            try:
                pto.unlink()
            except FileNotFoundError:
                pass
            pto.symlink_to(pfrom)
            print(f"Link \"{pto}\" was created.")
            break
    else:
        print("Libreoffice scripts folder not found")