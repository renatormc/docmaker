from docmaker.gui import widgets as wt
from docmaker import DocModel
from settings import APPDIR

midia_otica_model = DocModel("Mídia ótica", main_template="midia_otica.docx", 
                             format="docx", lists_folder=APPDIR / "models/midia_otica/listas")

midia_otica_model.widgets= [
    [
       wt.SComboBox("n_midias", "Nº Mídias", choices="opcoes_midias"),
       wt.SCheckBox("compatado", label="Compactado", default=False)
    ],
    [
        wt.SArray('hashes', label="Hashes", widgets=[
           [
               wt.SText('id', label="ID", stretch=1),
               wt.SText('value', label='Valor', stretch=5)
           ]
       ], default=[
           {'id': '', 'value': ''}
       ])
    ]
]

