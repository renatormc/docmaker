from docmaker.gui.form import Form
from docmaker.gui import widgets as wt
from docmaker.gui.widgets.types import ValidationError
from docmaker.converters import StringListConverter


def convert_pericia(value: str) -> dict:
    ret = {}
    try:
        parts = value.split("/")
        ret['seq'], ret['rg'], ret['ano'] = int(parts[0]), int(parts[1]), int(parts[2])
        return ret
    except:
        raise ValidationError("Valor incorreto")

        
class Form(Form):
    name = "Base"
    widgets = [
        [
            wt.SText("pericia", label="Pericia", placeholder="SEQ/RG/ANO", converter=convert_pericia),
            wt.SText("procedimento", label="Procedimento", placeholder="RAI ou inquérito"),
            wt.SSpinBox("n_objetos", label="N de objetos", required=True, default=1)
        ],
        [
            wt.SText("relatores", label="Relatores", placeholder="Relatores separados por vírgula", required=True, converter=StringListConverter()),
            wt.SText("revisores", label="Revisores", placeholder="Revisores separados por vírgula", converter=StringListConverter()),
        ],

    ]

    def pre_process(self, context: dict) -> dict:
        context['peritos'] = context['relatores'] + context['revisores']
        return context
