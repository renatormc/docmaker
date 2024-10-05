from docmaker.gui import widgets as wt
from docmaker.gui.widgets.types import ValidationError
from docmaker.converters import StringListConverter, DateConverter, PicsAnalyzer
from docmaker import DocModel
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


laudo_model = DocModel(
    "Laudo",
    format="docx",
    filename_in_workdir="laudo.docx",
    main_template="main_generic.docx"
)


laudo_model.widgets = [
    [
        wt.SText("pericia", label="Pericia",
                 placeholder="SEQ/RG/ANO", converter=convert_pericia),
        wt.SText("procedimento", label="Procedimento",
                 placeholder="RAI ou inquérito"),
        wt.SText("requisitante", label="Requisitante",
                 placeholder="Delegacia ou judiciário", stretch=1),
    ],
    [
        wt.SText("inicio_exame", label="Inicio Exame",
                 converter=DateConverter()),
        wt.SText("data_recimento", label="data de recebimento",
                 converter=DateConverter()),
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
]


@laudo_model.pre_process()
def pre_process(context):
    WORKDIR = Path(".").absolute()
    context['peritos'] = context['relatores'] + context['revisores']
    context['objetos'] = PicsAnalyzer("fotos", prefix="Objeto")(WORKDIR)
    context['n_objetos'] = len(context['objetos'])
    return context


@laudo_model.initial_load()
def initial_load():
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
        'procedimento': f"RAI {data.rai}",
        'pessoas_envolvidas': ", ".join(data.pessoas)
    }
