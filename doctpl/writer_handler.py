import os
import subprocess
import config
from pathlib import Path
from datetime import datetime
import json

class WriterHandler:
    def __init__(self) -> None:
        self.current_run_file: Path | None = None

    def _run_macro(self, url):
        if os.name == "nt":
            url = url.replace("\"", "\\\"")
            text = f"vnd.sun.star.script:{url}?language=Python&location=user"
            res = subprocess.check_output([config.LOFFICE_EXE, text])
        else:
            cmd = f"soffice 'vnd.sun.star.script:{url}?language=Python&location=user'"
            os.system(cmd)

    def run_macro(self, func: str, *args, **kwargs) -> None:
        import base64
        data = {"func": func, "args": args, "kwargs": kwargs}
        json_str = json.dumps(data)
        base64_encoded = base64.b64encode(json_str.encode('utf-8')).decode('utf-8')
        url = f"doctpl.py$run_func('{base64_encoded}')"
        self._run_macro(url)
        