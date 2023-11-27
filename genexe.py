import subprocess
from pathlib import Path
from docmaker.config import get_config
import sys
import os

cf = get_config()
template = Path("./docmaker.go")
srcfile = cf.local_folder / "docmaker.go"
text = template.read_text(encoding="utf-8")
scriptFile = Path("./main.py").absolute()
text = text.replace("$pythonExe", sys.executable.replace("\\", "\\\\")).replace(
    "$scriptFile", str(scriptFile).replace("\\", "\\\\"))
srcfile.write_text(text)

destexe = Path(input("Destination executable: ")) if len(sys.argv) == 1 else Path(sys.argv[1])
args = ['go', 'build', '-ldflags', '-H=windowsgui', '-o', str(destexe),  str(srcfile)] 
subprocess.run(['go', 'build', '-o', str(destexe),  str(srcfile)])
if os.name == "nt":
    exew = destexe.parent / f"{destexe.stem}w.exe"
    subprocess.run(['go', 'build', '-o', str(exew),  str(srcfile)])
