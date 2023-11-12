from doctpl.gui.form import BaseForm
from doctpl.gui import widgets as wt
from doctpl.gui.widgets.types import ValidationError


def convert_pericia(value: str) -> dict:
    ret = {}
    try:
        parts = value.split("/")
        ret['seq'], ret['rg'], ret['ano'] = int(parts[0]), int(parts[1]), int(parts[2])
        return ret
    except:
        raise ValidationError("Valor incorreto")


class Form(BaseForm):
    name = "Base"
    widgets = [
        [
            wt.SText("pericia", label="Pericia", converter=convert_pericia),
            wt.SSpinBox("n_objetos", label="N de objetos", required=True)
        ],

    ]
