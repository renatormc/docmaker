from pathlib import Path
import subprocess
from docmaker.config import get_config
import os
import json
from typing import Any, Literal
from docmaker.custom_types import FormatType

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


def open_writer(path: Path | None = None) -> None:
    args = [get_config().loffice_exe, "--writer"]
    if path:
        args.append(str(path))
    subprocess.Popen(args)


def open_in_filemanager(path: Path) -> None:
    if os.name == "nt":
        subprocess.Popen(['explorer.exe', str(path)])
    else:
        subprocess.run(['xdg-open', str(path)])


def open_file(path: Path, format: FormatType) -> None:
    if os.name == "nt":
        if format == "docx":
            # subprocess.run([f"{os.getenv('ProgramFiles')}\\ONLYOFFICE\\DesktopEditors\\DesktopEditors",
            #                "--ascdesktop-support-debug-info", str(path)])
            os.startfile(path) #type: ignore
        else:
            open_writer(path)
    else:
        if format == "odt":
            open_writer(path)
        else:
            subprocess.run(['xdg-open', str(path)])


def read_json_file(path: Path | str) -> Any:
    with Path(path).open("r", encoding="utf-8") as f:
        return json.load(f)


def write_json_file(path: Path | str, data: Any) -> None:
    with Path(path).open("w", encoding="utf-8") as f:
        f.write(json.dumps(data, ensure_ascii=False, indent=4, default=str))
