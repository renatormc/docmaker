from pathlib import Path
from docmaker.config import LIBDIR
import os

def link_lo_macro():
    folder = Path.home()
    pfrom = LIBDIR / "macros/docmaker.py"
    user = os.getlogin()
    aux = f"C:/Users/{user}/AppData/Roaming/LibreOffice/4/user/Scripts/python/docmaker.py"
    pto = Path(aux) if os.name == "nt" else folder / ".config/libreoffice/4/user/Scripts/python/docmaker.py"
    try:
        pto.parent.mkdir(parents=True)
    except FileExistsError:
        pass
    try:
        pto.unlink()
    except FileNotFoundError:
        pass
    pto.symlink_to(pfrom)
    print(f"Link \"{pto}\" was created.")
