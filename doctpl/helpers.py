from doctpl.gui.form import BaseForm
import importlib.util
from pathlib import Path

def inspect_models_folder(models_folder: Path) -> list[BaseForm]:
    forms: list[BaseForm] = []
    for entry in models_folder.iterdir():
        path = entry / "form.py"
        if path.exists():
            spec = importlib.util.spec_from_file_location(entry.name, path.absolute())
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            loaded_class = getattr(module, "Form")

            forms.append(loaded_class)
    return forms