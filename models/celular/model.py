from doctpl.gui import widgets as wt
from doctpl.gui.widgets.types import ValidationError
from doctpl.converters import StringListConverter, DateConverter, PicsAnalyzer
from doctpl import DocModel
from settings import APPDIR
from pathlib import Path

def convert_pericia(value: str) -> dict:
    ret = {}
    try:
        parts = value.split("/")
        ret['seq'], ret['rg'], ret['ano'] = int(
            parts[0]), int(parts[1]), int(parts[2])
        return ret
    except:
        raise ValidationError("Valor incorreto")


celular_model = DocModel(
    "Celular", 
    templates_folder=APPDIR / "models/celular/templates",
    lists_folder=APPDIR / "models/celular/listas",
)

def ler_requisicao():
    from doctpl.collectors.odin_pdf_parser import OdinPdfParser
    workdir: str | Path | None = celular_model.get_field_value("workdir")
    if workdir is None:
        return
    path = Path(workdir) / "Requisicao.pdf"
    if not path.is_file():
        return
    parser = OdinPdfParser(path)
    data = parser.extract_all()
    result = {
        'pericia': str(data.pericia),
        'requisitante': data.quesito.unidade_origem,
        'procedimento': f"RAI {data.rai}",
        'ocorrencia_odin': data.ocorrencia,
        'data_odin': data.data_ocorrencia,
        'n_quesito': data.quesito.numero,
        'autoridade': data.quesito.responsavel,
        'pessoas_envolvidas': ", ".join(data.pessoas)
        }
    return celular_model.load_data(result)

celular_model.widgets = [
    [
        wt.SFileChooser("workdir",label="Pasta de trabalho", required=True, type="dir", 
                        default=Path(".").absolute(), stretch=3),
        wt.SButton("Ler requisição", on_click=ler_requisicao, stretch=1),        
    ],
    [
        wt.SText("pericia", label="Pericia", placeholder="SEQ/RG/ANO", converter=convert_pericia),
        wt.SText("requisitante", label="Requisitante"),
        wt.SText("procedimento", label="Procedimento", placeholder="RAI ou inquérito"),
        wt.SText("ocorrencia_odin", label="Ocorrência ODIN")
    ],
    [
        wt.SText("data_odin", label="Data ODIN", converter=DateConverter()),
        wt.SText("inicio_exame", label="Inicio Exame", converter=DateConverter()),
        wt.SText("data_recimento", label="data de recebimento", converter=DateConverter()),
    ],
    [
        wt.SText("n_quesito", label="Número quesito"),
        wt.SText("autoridade", label="Autoridade"),
    ],
    [
        wt.SText("relatores", label="Relatores", placeholder="Relatores separados por vírgula",
                 required=True, converter=StringListConverter()),
        wt.SText("revisores", label="Revisores", placeholder="Revisores separados por vírgula", converter=StringListConverter()),
    ],
    [
        wt.SText("lacre_entrada", label="Lacre entrada"),
        wt.SText("lacre_saida", label="Lacre saída"),
        wt.SComboBox("n_midias", "Nº Mídias", choices="opcoes_midias")
    ]

]

@celular_model.pre_process()
def pre_process(context):
    context['peritos'] = context['relatores'] + context['revisores']
    context['objetos'] = PicsAnalyzer("fotos", prefix="Celular")(context['workdir'])
    context['n_objetos'] = len(context['objetos'])
    return context

