from pathlib import Path
import hashlib
from docmaker.config import get_config

def get_files_dir_path(path: Path) -> Path:
    hash = hashlib.md5()
    hash.update(str(path).encode('utf-8'))
    hashed_string = hash.hexdigest()
    return get_config().tempdir / hashed_string