from pathlib import Path
import os
from typing import Literal


APPDIR = Path(os.path.dirname(os.path.realpath(__file__)))


class Config:
    def __init__(self) -> None:
        self.loffice_exe = ""
        self.env: Literal['prod', 'dev'] = "prod"
    
        
_config = Config()

def get_config() -> Config:
    return _config


    
    
