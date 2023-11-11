from com.sun.star.text.TextContentAnchorType import AS_CHARACTER
from com.sun.star.awt import Size
from pathlib import Path
import re
import logging
import os
import json
from pathlib import Path
import tempfile
import subprocess
from uuid import uuid4
import shutil


class Helper:
    def __init__(self, files_dir=None) -> None:
        self.doc = XSCRIPTCONTEXT.getDocument()
        self.files_dir = Path(files_dir) if files_dir else self.get_docdir()
        path = Path.home() / ".rmc/log/doctpl.log"
        try:
            path.parent.mkdir(parents=True)
        except FileExistsError:
            pass
        logging.basicConfig(filename=str(
            path), encoding='utf-8', level=logging.DEBUG)
        logging.info("Teste")
        self.render_info = self.read_info()
        self.doctpl_config = self.read_doctpl_config()

    def read_doctpl_config(self):
        path = Path.home() / ".rmc/etc/doctpl.json"
        if path.exists():
            with path.open("r", encoding="utf-8") as f:
                data = json.load(f)
            return data

    def read_info(self):
        path = self.file_path("info.json")
        if path.exists():
            with path.open("r", encoding="utf-8") as f:
                data = json.load(f)
            return data

    def get_docdir(self) -> Path:
        dir_ = self.doc.getURL()
        if os.name == "nt":
            return Path(dir_.replace("file:///", "")).parent
        return Path(dir_.replace("file://", "")).parent

    def file_path(self, relpah) -> Path:
        return self.files_dir / relpah

    def get_subdoc_url(self, name) -> str:
        aux = self.doc.getURL()
        return f"{aux}/subdocs/{name}"

    def add_image(self, path, w, h, cur):
        path = Path(path).absolute()
        if not path.exists():
            print(f"File {path} do not exist")
        img = self.doc.createInstance('com.sun.star.text.TextGraphicObject')
        img.GraphicURL = path.as_uri()
        img.setPropertyValue('AnchorType', AS_CHARACTER)
        width = w*100
        alfa = width/w
        cur.setString("")
        cur.Text.insertTextContent(cur, img, False)
        height = alfa*h
        img.setSize(Size(width, height))

    def add_subdoc(self, name: str, cur):
        path = self.file_path(f"subdocs/{name}")
        cur.setString("")
        cursor = cur.Text.createTextCursor()
        cursor.gotoEnd(False)
        cursor.insertDocumentFromURL(path.as_uri(), ())

    def replace_action(self, action, args, cur):
        if action == "image":
            data = self.render_info['pics'][args[0]]
            self.add_image(data['path'], data['w'], data['h'], cur)
        if action == "subdoc":
            self.add_subdoc(args[0], cur)

    def pos_process(self):
        replace = self.doc.createReplaceDescriptor()
        replace.SearchRegularExpression = True
        reg = r'@(.{1,15}?)\((.{1,100}?)\)'
        replace.SearchString = reg
        selsFound = self.doc.findAll(replace)
        for i in range(0, selsFound.getCount()):
            selFound = selsFound.getByIndex(i)
            name = selFound.getString().strip()
            res = re.search(reg, name)
            action, args = res.group(1), res.group(2).split(",")
            args = [arg.strip() for arg in args]
            self.replace_action(action, args, selFound)


def pos_process():
    helper = Helper()
    helper.pos_process()


def add_document():
    helper = Helper()
    try:
        temp_dir = Path(tempfile.gettempdir()) / uuid4().hex
        logging.info(f"Creating \"{temp_dir}\"")
        os.system(f"doctpl.ps1 gui -d \"{temp_dir}\"")
        project_folder = Path(
            helper.doctpl_config['python_interpreter']).parent.parent.parent
        python = project_folder / \
            ".venv/Scripts/python.exe" if os.name == "nt" else project_folder / ".venv/bin/python"
        logging.info(str(python))
        subprocess.Popen(
            ["cmd", "/K", str(python), str(project_folder / "main.py"), 'gui', '-d', str(temp_dir)])
    finally:
        try:
            logging.info(f"Removing \"{temp_dir}\"")
            shutil.rmtree(temp_dir)
        except FileNotFoundError:

            pass
