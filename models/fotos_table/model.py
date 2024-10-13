from docmaker.gui import widgets as wt
from docmaker import DocModel
from settings import APPDIR
from pathlib import Path
from docmaker.converters import IntConverter

fotos_table_model = DocModel("Tabela fotos",
                             templates_folder=APPDIR / "models/fotos_table/templates",
                             format="docx",
                             main_template="main.docx",
                             filename_in_workdir="",
                             )

fotos_table_model.widgets = [

    [
        wt.SFileChooser("files", label="Pasta com fotos", type="dir", required=True, stretch=3),
        wt.SText("width", label="Largura total", placeholder="Em milímetros", converter=IntConverter(default=-1), stretch=1, default=80)
    ],
    [
        wt.SText("caption", label="Legenda", stretch=4),
        wt.SSpinBox("n_cols", "Número de colunas", default=2, min=1, max=3, stretch=1),
        wt.SComboBox("show_caption", label="", choices=['Nâo incluir nome', 'Incluir nome com extensão', 'Incluir nome sem extensão', 'Usar mesma legenda'])
    ],

]

def get_name(p: Path, show_caption: str, caption: str):
    if show_caption == "Incluir nome com extensão":
        return p.name
    if show_caption == "Incluir nome sem extensão":
        return p.stem
    if show_caption == "Usar mesma legenda":
        return caption
    return ""

@fotos_table_model.pre_process()
def pre_process(context):
    w = 150
    if context['width'] == -1:
        if context['n_cols'] == 2:
            w = 80
    else:
        w = int(context['width']/context['n_cols'])
    context['show_table_caption'] = bool(context['caption'] != "" and context['show_caption'] != "Usar mesma legenda")
    context['pics'] = [{'path': str(f), 'caption': get_name(f, context['show_caption'], context['caption']), 'width': w} for f in Path(context['files']).iterdir()]
    return context
