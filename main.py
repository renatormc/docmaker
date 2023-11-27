from docmaker import App
from models.laudo.model import laudo_model
from models.test.model import test_model
from models.fotos_table.model import fotos_table_model
from models.objetos_celular.model import objeto_celular_model
import settings
import sys
import os

if len(sys.argv) > 1:
    os.chdir(sys.argv[1])


app = App()
app.set_templates_folder(settings.APPDIR / "models/templates")
app.set_env(settings.ENV)

app.add_docmodel(laudo_model)
app.add_docmodel(test_model)
app.add_docmodel(fotos_table_model)
app.add_docmodel(objeto_celular_model)

app.run_gui()  
   
   