from docmaker.gui import widgets as wt
from docmaker import DocModel
from pathlib import Path
from docmaker.converters import PicsAnalyzer

objeto_celular_model = DocModel("Objetos celular", main_template="celular_objetos.odt", format="odt")

objeto_celular_model.widgets= [
    [
        wt.SFileChooser("objetos", label="Pasta fotos", type="dir", required=True, 
                        converter=PicsAnalyzer("fotos", prefix="Objeto"),
                        default=str(Path(".").absolute())),
        wt.SSpinBox("n_col_fotos", label="N Col Fotos", min=1, max=2, default=2)
    ]
]

@objeto_celular_model.pre_process()
def pre_process(context):
    context['n_objetos'] = len(context['objetos'])
    context['pics_width'] = int(150/context['n_col_fotos'])
    return context
