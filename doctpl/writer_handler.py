import os
import subprocess
import config
from pathlib import Path

class WriterHandler:
    def __init__(self) -> None:
        pass

    def run_macro(self, url):
        if os.name == "nt":
            url = url.replace("\"", "\\\"")
            text = f"vnd.sun.star.script:{url}?language=Python&location=user"
            print(text)
            res = subprocess.check_output([config.LOFFICE_EXE, text])
            print(res)
        else:
            cmd = f"soffice 'vnd.sun.star.script:{url}?language=Python&location=user'"
            os.system(cmd)

    def pos_process(self, files_folder: Path):
        url = f"doctpl.py$pos_process(\"{files_folder}\")"
        print(url)
        self.run_macro(url)

    def add_doc(self, path: Path):
        url = f"doctpl.py$add_doc(\"{path}\")"
        self.run_macro(url)