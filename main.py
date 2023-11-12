import argparse
from pathlib import Path
import config
import os
import actions as act
import logging

logging.basicConfig(filename=str(config.LOCAL_FOLDER / "doctpl.log"), encoding='utf-8', level=logging.DEBUG)

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

# p_gui = subparsers.add_parser("gui")
# p_gui.add_argument('filename')
# p_gui.add_argument("-d", "--dir", required=True, help="Directory to generate pre compiled files")

p_start = subparsers.add_parser("new")
p_start.add_argument('filename')

args = parser.parse_args()
match args.command:
    case "link-macro":
        link_macro()            
    # case "gui":
    #     act.show_gui(args.dir)
    case "new":
        path = Path(args.filename).absolute()
        if path.suffix == ".odt": 
            act.show_gui(path)
        else:
            print("the filename must have .odt extension")
   