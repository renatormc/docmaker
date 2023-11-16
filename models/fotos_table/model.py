from doctpl.gui import widgets as wt
from doctpl import DocModel
from settings import APPDIR
from pathlib import Path

fotos_table_model = DocModel("Tabela fotos",
                             templates_folder=APPDIR / "models/fotos_table/templates",
                             format="docx"
                             )

fotos_table_model.widgets = [

    [
        wt.SFileChooser("files", label="Pasta com fotos", type="dir", required=True)
    ],
    [
        wt.SText("caption", label="Legenda"),
        wt.SSpinBox("n_cols", "Número de colunas", default=2),
        wt.SCheckBox("show_caption", "incluir nome", default=False)
    ],

]

@fotos_table_model.pre_process()
def pre_process(context):
    w = int(160/context['n_cols'])
    context['pics'] = [{'path': str(f), 'caption': f.name, 'width': w} for f in Path(context['files']).iterdir()]
    return context
