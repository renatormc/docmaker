from doctpl.gui import widgets as wt
from doctpl import DocModel
from settings import APPDIR


test_model = DocModel("Test",
                      templates_folder=APPDIR / "models/test/templates",
                      format="odt"
                      )

test_model.widgets = [
    [
        wt.SText("names", label="Names", converter=lambda x: x.split(",")),
        wt.SFileChooser("myimage", label="Imagem")
    ],
    [
        wt.SArray("people", [
            [
                wt.SText("name", label="Name"),
                wt.SText("profession", label="Profession"),
            ]
        ], "People")
    ]
]


@test_model.pre_process()
def pre_process(context: dict) -> dict:
    context['title'] = "Título 1"
    return context
