from com.sun.star.text.TextContentAnchorType import AS_CHARACTER
from com.sun.star.awt import Size
from com.sun.star.beans import PropertyValue
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

    def add_subdoc_on_current_position(self, path: Path):
        current_controller = self.doc.getCurrentController()
        cur = current_controller.getViewCursor()
        cursor = cur.Text.createTextCursor()
        cursor.gotoEnd(False)
        cursor.insertDocumentFromURL(path.as_uri(), ())


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
    try:
        temp_dir = Path(tempfile.gettempdir()) / uuid4().hex
        helper = Helper(files_dir=temp_dir)
        logging.info(f"Creating \"{temp_dir}\"")
        temp_dir.mkdir()

        exe = Path.home() / ".local/bin/doctpl"
        subprocess.check_call([str(exe), 'gui', '-d', str(temp_dir)])
        helper.add_subdoc_on_current_position(temp_dir / "main.odt")
    finally:
        try:
            logging.info(f"Removing \"{temp_dir}\"")
            shutil.rmtree(temp_dir)
        except FileNotFoundError:

            pass
