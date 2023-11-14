import argparse
import actions as act
import logging
import sys
import subprocess
import settings

logging.basicConfig(filename=str(settings.LOCAL_FOLDER / "doctpl.log"), encoding='utf-8', level=logging.DEBUG)


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
        from doctpl import link_lo_macro
        link_lo_macro()            
    case "gui":
        act.show_gui()
    case "build":
        # args = ['go', 'build', '-ldflags', '-H=windowsgui', '-o', '.local/doctpl.exe', 'launcher.go']
        args = ['go', 'build', '-o', '.local/doctpl.exe', 'launcher.go']
        subprocess.run(args)        
   
   