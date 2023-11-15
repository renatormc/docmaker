# Doctpl

Doctpl is a framework to create forms to generate docx documents. It uses docxtpl and pyside6 libs.

# Creating models

In order to create a model you have to create a new instance of DocModel defining the templates folder and the widget matrix as example below.

```python
from doctpl.gui import widgets as wt
from doctpl.gui.widgets.types import ValidationError
from doctpl.converters import StringListConverter, DateConverter
from doctpl import DocModel
from settings import APPDIR

def convert_pericia(value: str) -> dict:
    ret = {}
    try:
        parts = value.split("/")
        ret['seq'], ret['rg'], ret['ano'] = int(
            parts[0]), int(parts[1]), int(parts[2])
        return ret
    except:
        raise ValidationError("Valor incorreto")


celular_model = DocModel(
    "Celular", 
    templates_folder=APPDIR / "models/celular/templates",
    lists_folder=APPDIR / "models/celular/listas",
)

celular_model.widgets = [
    [
        wt.SText("pericia", label="Pericia", placeholder="SEQ/RG/ANO", converter=convert_pericia),
        wt.SText("requisitante", label="Requisitante"),
        wt.SText("procedimento", label="Procedimento", placeholder="RAI ou inquérito"),
        wt.SText("ocorrencia_odin", label="Ocorrência ODIN"),
        wt.SSpinBox("n_objetos", label="N de objetos", required=True, default=1)
    ],
    [
        wt.SText("data_odin", label="Data ODIN", converter=DateConverter()),
        wt.SText("inicio_exame", label="Inicio Exame", converter=DateConverter()),
        wt.SText("data_recimento", label="data de recebimento", converter=DateConverter()),
    ],
    [
        wt.SText("n_quesito", label="Número quesito"),
        wt.SText("autoridade", label="Autoridade"),
    ],
    [
        wt.SText("relatores", label="Relatores", placeholder="Relatores separados por vírgula",
                 required=True, converter=StringListConverter()),
        wt.SText("revisores", label="Revisores", placeholder="Revisores separados por vírgula", converter=StringListConverter()),
    ],
    [
        wt.SText("lacre_entrada", label="Lacre entrada"),
        wt.SText("lacre_saida", label="Lacre saída"),
        wt.SComboBox("n_midias", "Nº Mídias", choices="opcoes_midias")
    ]

]

@celular_model.pre_process()
def pre_process(context):
    context['peritos'] = context['relatores'] + context['revisores']
    return context
```

# Run the app

You have to create an app and register all your models like below:

```python
from doctpl import App
from models.celular.model import celular_model
from models.test.model import test_model
import settings

app = App(settings.LOCAL_FOLDER)
app.set_env(settings.ENV)

app.add_docmodel(celular_model)
app.add_docmodel(test_model)

app.run_gui()  
```

# .env

```
ENV=dev
DOCTPL_LOCAL_FOLDER=/path/to/.local
```

# Link macro

If you are gonna use LibreOffice you will need to make use of some macros, so you have to install the extension APSO and execute the command below to link the macros inside libreoffice.

```
python -m doctpl link-macro
```
