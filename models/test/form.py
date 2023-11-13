from doctpl.gui.form import BaseForm
from doctpl.gui import widgets as wt


class Form(BaseForm):
    name = "Teste"
    widgets = [
        [
            wt.SText("names", label="Names", converter=lambda x: x.split(",")),
        ],
    ]

    def pre_process(self, context: dict) -> dict:
        context['title'] = "Título 1"
        return context
