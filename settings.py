from pathlib import Path
import os
from doctpl.custom_types import EnvType
from dotenv import load_dotenv
load_dotenv()


APPDIR = Path(os.path.dirname(os.path.realpath(__file__)))
LOCAL_FOLDER = APPDIR / ".local"
ENV: EnvType = os.getenv("ENV") or "prod"


