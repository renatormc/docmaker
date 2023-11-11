from doctpl.gui.form import BaseForm
from doctpl.gui import widgets as wt


class Form(BaseForm):
    name = "Teste"
    widgets = [
        [
            wt.SText("name", label="Name"),
        ],

    ]
