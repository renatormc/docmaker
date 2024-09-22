from pathlib import Path
import re
from pdfminer.high_level import extract_text
from .data_types import OdinParserData


class Parser2:
    def get_ocorrencia(self, text: str) -> str:
        res = re.search(r'Ocorrência nº:(.+)', text)
        if res:
            return res.group(1).strip()
        return ""

    def get_responsavel(self, text: str) -> str:
        res = re.search(r'Responsável:(.+)', text)
        if res:
            return res.group(1).strip()
        return ""

    def get_data_criacao(self, text: str) -> str:
        res = re.search(r'Data de criação:(.+)', text)
        if res:
            return res.group(1).strip().split()[0]
        return ""

    def get_data_ocorrencia(self, text: str) -> str:
        res = re.search(r'Histórico incluído em:(.+)', text)
        if res:
            return res.group(1).strip().split()[0]
        return ""

    def get_rai(self, text: str) -> str:
        res = re.search(r'RAI:(.+)', text)
        if res:
            return res.group(1).strip()
        return ""

    def get_unidade_origem(self, text: str) -> str:
        res = re.search(r'Unidade de origem:(.+)', text)
        if res:
            return res.group(1).strip()
        return ""

    def get_pessoas_envolvidas(self, text: str):
        res = re.findall(r'(.+?\((.+?)\))', text.split("Pessoas")[1])
        pessoas = []
        for item in res:
            aux = item[1].strip()
            if aux in ['AUTOR', 'ENVOLVIDO']:
                pessoas.append(item[0])
        return pessoas

    def get_conteudo_quesito(self, text: str) -> str:
        res = re.search(r'Conteúdo:(.+)Perícia vinculada:', text, re.DOTALL)
        if res:
            return res.group(1).strip()
        return ""


class OdinPdfParser:
    def __init__(self, file_: str | Path) -> None:
        self.file_ = Path(file_)
        self.reg1 = r'REQUISIÇÃO DE PERÍCIA(.+)Histórico(.+)Quesitos vinculados(.+)Equipe Envolvida(.+)Pessoas(.+)Vestígios/Exames(.+)'
        self.text = extract_text(self.file_)
        self.parts_res = re.search(self.reg1, self.text, re.MULTILINE | re.DOTALL)

    def change_string_case(self, value: str) -> str:
        text = value.title()
        parts = text.split()
        for i, p in enumerate(parts):
            if p in ['Da', 'Do', "Dos", "De"]:
                parts[i] = p.lower()
        return " ".join(parts)

    def extract_all(self) -> OdinParserData:
        if not self.parts_res:
            return self.extract_all2()
        data = OdinParserData()

        text = self.parts_res.group(1)
        aux = "LABORATÓRIO" if "LABORATÓRIO" in text else "SEÇÃO"
        reg = aux + r'.*- ICLR.*?(\d+/\d+) RG (\d+/\d+).*Ocorrência: (\d+/\d+).*?(\d+/\d+/\d+).*RAI: (\d+).*Unidade Solicitante: (.+?)\s*Autoridade: (.+?)\s*Tipificações.*'
        res = re.search(reg, text, re.MULTILINE | re.DOTALL)

        if res:

            try:
                parts1 = res.group(1).split("/")
                parts2 = res.group(2).split("/")
                data.pericia.seq = int(parts1[0])
                data.pericia.rg = int(parts2[0])
                data.pericia.ano = int(parts2[1])
            except:
                pass
            data.ocorrencia = res.group(3)
            data.data_ocorrencia = res.group(4)
            data.rai = res.group(5)
            data.unidade_solicitante = self.change_string_case(res.group(6))
            data.autoridade = self.change_string_case(res.group(7))

        text = self.parts_res.group(3)
        reg = r'Quesito n.: (\d+).*Data de criação: (\d+/\d+/\d+).*Responsável pelo quesito: (.+?)\s*Unidade de origem: (.+?)\s*Unidade afeta:.*Conteúdo: (.+)'
        res = re.search(reg, text, re.MULTILINE | re.DOTALL)
        if res:
            data.quesito.numero = res.group(1)
            data.quesito.data_criacao = res.group(2)
            data.quesito.responsavel = self.change_string_case(res.group(3))
            data.quesito.unidade_origem = self.change_string_case(res.group(4))
            data.quesito.conteudo = res.group(5)

        text = self.parts_res.group(5)
        reg = r'(.+) \(.+\)'
        res2 = re.findall(reg, text)
        if res2:
            data.pessoas = [self.change_string_case(p) for p in res2]

        return data

    def extract_all2(self) -> OdinParserData:
        data = OdinParserData()
        parser2 = Parser2()
        data.ocorrencia = parser2.get_ocorrencia(self.text)
        data.data_ocorrencia = parser2.get_data_ocorrencia(self.text)
        data.rai = parser2.get_rai(self.text)
        data.unidade_solicitante = parser2.get_unidade_origem(self.text)
        data.autoridade = parser2.get_responsavel(self.text)
        data.pessoas = parser2.get_pessoas_envolvidas(self.text)
        data.quesito.data_criacao = parser2.get_data_criacao(self.text)
        data.quesito.responsavel = data.autoridade
        data.quesito.conteudo = parser2.get_conteudo_quesito(self.text)
        return data
