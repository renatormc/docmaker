from doctpl import App
from models.celular.model import celular_model
from models.test.model import test_model
import settings

def show_gui():
    app = App(settings.LOCAL_FOLDER, settings.LOFFICE_EXE)
    app.set_env(settings.ENV)
   
    app.add_docmodel(celular_model)
    app.add_docmodel(test_model)
    
    app.run_gui()