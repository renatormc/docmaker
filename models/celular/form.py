from doctpl.gui.form import BaseForm
from doctpl.gui import widgets as wt


class Form(BaseForm):
    name = "Celular"
    widgets = [
        [
            wt.SText("pericia", label="Pericia"),
            wt.SText("pericia", label="Pericia")
        ],

    ]
