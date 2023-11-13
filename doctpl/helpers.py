from doctpl.gui.form import BaseForm
import importlib.util
from pathlib import Path
import subprocess
import config

def inspect_models_folder(models_folder: Path) -> list[BaseForm]:
    forms: list[BaseForm] = []
    for entry in models_folder.iterdir():
        path = entry / "form.py"
        if path.exists():
            spec = importlib.util.spec_from_file_location(
                entry.name, path.absolute())
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            loaded_class: BaseForm = getattr(module, "Form")
            loaded_class.templates_dir = entry / "templates"
            forms.append(loaded_class)
    return forms


def folder_in_path(folder_path):
    powershell_command = f'$env:Path -split \';\' -contains "{folder_path}"'

    try:
        result = subprocess.run(
            ["powershell", "-Command", powershell_command], capture_output=True, text=True, check=True)
        return result.stdout.strip().lower() == 'true'
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return False


def add_to_path(folder_path):
    if not folder_in_path(folder_path):
        powershell_command = f'[System.Environment]::SetEnvironmentVariable("Path", $env:Path + ";{folder_path}", [System.EnvironmentVariableTarget]::User)'

        try:
            subprocess.run(["powershell", "-Command",
                           powershell_command], check=True)
            print(
                f"The folder {folder_path} has been added to the PATH variable for the current user.")
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")
    else:
        print(
            f"The folder {folder_path} is already in the PATH variable for the current user.")
        
def open_doc(path: Path) -> None:
    subprocess.Popen([config.LOFFICE_EXE, "--writer", str(path)])
