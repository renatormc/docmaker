from docmaker.gui import widgets as wt
from docmaker.gui.widgets.widget import Widget
from docmaker.gui.widgets.types import ValidationError
from docmaker.converters import StringListConverter, DateConverter, PicsAnalyzer
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


common_widgets: list[list[Widget]] = [
    [
        wt.SText("pericia", label="Pericia",
                 placeholder="SEQ/RG/ANO", converter=convert_pericia),
        wt.SText("requisitante", label="Requisitante"),
        wt.SText("procedimento", label="Procedimento",
                 placeholder="RAI ou inquérito"),
        wt.SText("ocorrencia_odin", label="Ocorrência ODIN")
    ],
    [
        wt.SText("data_odin", label="Data ODIN", converter=DateConverter()),
        wt.SText("inicio_exame", label="Inicio Exame",
                 converter=DateConverter()),
        wt.SText("data_recimento", label="data de recebimento",
                 converter=DateConverter()),
    ],
    [
        wt.SText("n_quesito", label="Número quesito"),
        wt.SText("autoridade", label="Autoridade"),
    ],
    [
        wt.SText("pessoas_envolvidas", label="Pessoas envolvidas",
                 converter=StringListConverter())
    ],
    [
        wt.SText("relatores", label="Relatores", placeholder="Relatores separados por vírgula",
                 required=True, converter=StringListConverter()),
        wt.SText("revisores", label="Revisores",
                 placeholder="Revisores separados por vírgula", converter=StringListConverter()),
    ],
    [
        wt.SText("lacre_entrada", label="Lacre entrada"),
        wt.SText("lacre_saida", label="Lacre saída"),
        wt.SComboBox("n_midias", "Nº Mídias", choices="opcoes_midias"),
    ]
]

def common_pre_process(context):
    context['peritos'] = context['relatores'] + context['revisores']
    WORKDIR = Path(".").absolute()
    context['objetos'] = PicsAnalyzer("fotos", prefix="Celular")(WORKDIR)
    context['n_objetos'] = len(context['objetos'])
    return context

def common_initial_load():
    from docmaker.collectors.odin_pdf_parser import OdinPdfParser
    WORKDIR = Path(".").absolute()
    path = WORKDIR / "Requisicao.pdf"
    print(path)
    if not path.is_file():
        return
    parser = OdinPdfParser(path)
    data = parser.extract_all()
    return {
        'pericia': str(data.pericia),
        'requisitante': data.quesito.unidade_origem,
        'procedimento': f"RAI {data.rai}",
        'ocorrencia_odin': data.ocorrencia,
        'data_odin': data.data_ocorrencia,
        'n_quesito': data.quesito.numero,
        'autoridade': data.quesito.responsavel,
        'pessoas_envolvidas': ", ".join(data.pessoas)
    }