# Docmaker

Docmaker is a framework to create forms to generate docx documents. It uses docxtpl and pyside6 libs.

# Creating models

In order to create a model you have to create a new instance of DocModel defining the templates folder and the widget matrix as example below.

```python
# app.py
from docmaker.gui import widgets as wt
from docmaker.gui.widgets.types import ValidationError
from docmaker.converters import StringListConverter, DateConverter
from docmaker import DocModel
from docmaker import App
from pathlib import Path
import os

SCRIPT_DIR = Path(os.path.dirname(os.path.realpath(__file__)))

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
    templates_folder=SCRIPT_DIR / "models/celular/templates",
    lists_folder=SCRIPT_DIR / "models/celular/listas",
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

app = App()
app.set_env("dev")
app.add_docmodel(celular_model)
app.run_gui()  
```


# Run application

```bash
python app.py
```