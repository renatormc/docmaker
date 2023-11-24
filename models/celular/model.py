from docmaker.gui import widgets as wt
from docmaker.gui.widgets.types import ValidationError
from docmaker.converters import StringListConverter, DateConverter, PicsAnalyzer
from docmaker import DocModel
from settings import APPDIR
from pathlib import Path
from models.common_widgets import common_widgets, common_pre_process, common_initial_load

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
    lists_folder=APPDIR / "models/celular/listas",
    format="odt",
    filename_in_workdir="laudo.odt",
    main_template="main_generic.odt"
)


celular_model.widgets = [
   *common_widgets,
   [
       wt.SSpacer(stretch=1),
       wt.SSpinBox("n_col_fotos", label="Colunas fotos", min=1, max=2)
   ]
]


@celular_model.pre_process()
def pre_process(context):
    context = common_pre_process(context)
    context['objetos_subdoc'] = "celular_objetos.odt"
    context['pics_width'] = int(150/context['n_col_fotos'])
    return context


@celular_model.initial_load()
def initial_load():
    return common_initial_load()
