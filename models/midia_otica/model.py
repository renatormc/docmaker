from docmaker.gui import widgets as wt
from docmaker import DocModel
from settings import APPDIR

midia_otica_model = DocModel("Mídia ótica", main_template="midia_otica.docx", 
                             format="docx", lists_folder=APPDIR / "models/midia_otica/listas")

midia_otica_model.widgets= [
    [
       wt.SComboBox("n_midias", "Nº Mídias", choices="opcoes_midias"),
    ]
]

