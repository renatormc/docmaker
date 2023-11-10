from pathlib import Path
import os

LIBDIR = Path(os.path.dirname(os.path.realpath(__file__)))
aux = os.getenv("MODELS_DIR")
MODELS_DIR = Path(aux) if aux else LIBDIR.parent / "models"
