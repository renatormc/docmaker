from doctpl.gui import widgets as wt
from doctpl import DocModel
from settings import APPDIR


test_model = DocModel("Test", templates_folder=APPDIR /
                      "models/test/templates")

test_model.widgets = [
    [
        wt.SText("names", label="Names", converter=lambda x: x.split(",")),
    ],
]


@test_model.pre_process()
def pre_process(context: dict) -> dict:
    context['title'] = "Título 1"
    return context
