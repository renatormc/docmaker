from doctpl import App
from models.celular.model import celular_model
from models.test.model import test_model
from models.fotos_table.model import fotos_table_model
import settings

app = App()
app.set_env(settings.ENV)

app.add_docmodel(celular_model)
app.add_docmodel(test_model)
app.add_docmodel(fotos_table_model)

app.run_gui()  
   
   