import subprocess
from pathlib import Path
import settings
import sys

template = Path("./docmaker.go")
srcfile = settings.LOCAL_FOLDER / "docmaker.go"
text = template.read_text(encoding="utf-8")
scriptFile = Path("./main.py").absolute()
text = text.format(pythonExe=sys.executable, scritpFile=str(scriptFile))
print(text)
# subprocess.run(['go'])