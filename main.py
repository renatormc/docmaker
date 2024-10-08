from operator import setitem
from docmaker import App
from models.laudo.model import laudo_model
from models.midia_otica.model import midia_otica_model
from models.fotos_table.model import fotos_table_model
from models.objetos_celular.model import objeto_celular_model
import settings
import os
import argparse
import subprocess

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(dest="command", required=True, help='Command to be used')

p_gui = subparsers.add_parser("gui")
p_gui.add_argument("-w", default=".", help="workdir")

p_templates = subparsers.add_parser("templates")

p_code = subparsers.add_parser("code")

p_update = subparsers.add_parser("update")

args = parser.parse_args()
if args.command == "gui":
    if args.w:
        os.chdir(args.w)    
    app = App()
    app.set_templates_folder(settings.APPDIR / "models/templates")
    app.set_env(settings.ENV)

    app.add_docmodel(laudo_model)
    app.add_docmodel(objeto_celular_model)
    app.add_docmodel(midia_otica_model)
    app.add_docmodel(fotos_table_model)

    app.run_gui()  
elif args.command == "templates":
    subprocess.Popen(['explorer.exe', str(settings.APPDIR / "models/templates")])
elif args.command == "code":
    os.system(f"code \"{settings.APPDIR}\"")
elif args.command == "update":
    os.chdir(str(settings.APPDIR))
    branch = subprocess.getoutput("git rev-parse --abbrev-ref HEAD")
    os.system("git reset --hard")
    os.system(f"git pull origin {branch}")
    
  
   
   