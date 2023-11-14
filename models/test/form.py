from doctpl.gui.form import Form
from doctpl.gui import widgets as wt


class Form(Form):
    name = "Teste"
    widgets = [
        [
            wt.SText("names", label="Names", converter=lambda x: x.split(",")),
        ],
    ]

    def pre_process(self, context: dict) -> dict:
        context['title'] = "Título 1"
        return context
