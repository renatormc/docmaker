from pathlib import Path
import os
from dotenv import load_dotenv
load_dotenv()

APPDIR = Path(os.path.dirname(os.path.realpath(__file__)))
LOCAL_FOLDER = APPDIR / ".local"
try:
    LOCAL_FOLDER.mkdir()
except FileExistsError:
    pass


