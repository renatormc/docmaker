import argparse
from pathlib import Path
import config
import os
import actions as act
import logging
import sys
import subprocess

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
p_build = subparsers.add_parser("build")

p_gui = subparsers.add_parser("gui")

if len(sys.argv) < 2:
    sys.argv.append("gui")
args = parser.parse_args()
match args.command:
    case "link-macro":
        link_macro()            
    case "gui":
        act.show_gui()
    case "build":
        # args = ['go', 'build', '-ldflags', '-H=windowsgui', '-o', '.local/doctpl.exe', 'launcher.go']
        args = ['go', 'build', '-o', '.local/doctpl.exe', 'launcher.go']
        subprocess.run(args)        
    # case "new":
    #     path = Path(args.filename).absolute()
    #     if path.suffix == ".odt": 
    #         act.show_gui(path)
    #     else:
    #         print("the filename must have .odt extension")
   