from pathlib import Path
import os
from doctpl.custom_types import EnvType
from dotenv import load_dotenv
load_dotenv()


APPDIR = Path(os.path.dirname(os.path.realpath(__file__)))
LOCAL_FOLDER = APPDIR / ".local"

LOFFICE_EXE = "soffice"
if os.name == "nt":
    aux = os.getenv("LOFFICE_EXE")
    if not aux:
        raise Exception("LOFFICE_EXE was not set")
    path = Path(aux).absolute()
    if not path.is_file() or path.suffix != ".exe":
        raise Exception(f"LOFFICE_EXE doesn't point to an exe file")
    LOFFICE_EXE = str(path)
ENV: EnvType = os.getenv("ENV") or "prod"


