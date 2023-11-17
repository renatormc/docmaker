from pathlib import Path
from typing import Literal
from docmaker.gui.widgets.types import ValidationError
from typing import TYPE_CHECKING



class PathConverter:
    def __init__(self, type_:Literal['dir', 'file'] = 'file') -> None:
        self.type_ =  type_
    
    def __call__(self,  value: str) -> Path|None:
        text = str(value).strip()
        if text == "":
            return None
        path = Path(text)
        if not path.exists():
            raise ValidationError("Caminho inexistente")
        if self.type_ == 'file' and not path.is_file():
            raise ValidationError("O endereço não é um endereço de arquivo válido")
        if self.type_ == 'dir' and not path.is_dir():
            raise ValidationError("O endereçõ não é um endereço de diretório válido")
        return path