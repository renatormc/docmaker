from pathlib import Path
import os
from typing import Literal
from dotenv import load_dotenv
load_dotenv()


APPDIR = Path(os.path.dirname(os.path.realpath(__file__)))
LOCAL_FOLDER = APPDIR / ".local"
TEMPDIR = LOCAL_FOLDER / "tmp"
try:
    TEMPDIR.mkdir(parents=True)
except FileExistsError:
    pass

LOFFICE_EXE = "soffice"
if os.name == "nt":
    aux = os.getenv("LOFFICE_EXE")
    if not aux:
        raise Exception("LOFFICE_EXE was not set")
    path = Path(aux).absolute()
    if not path.is_file() or path.suffix != ".exe":
        raise Exception(f"LOFFICE_EXE doesn't point to an exe file")
    LOFFICE_EXE = str(path)
ENV: Literal['prod', 'dev'] = os.getenv("ENV") or "prod"


