from com.sun.star.text.TextContentAnchorType import AS_CHARACTER
from com.sun.star.awt import Size
import uno
from pathlib import Path
import re
import logging
import os
import json
from pathlib import Path


XSCRIPTCONTEXT_ = XSCRIPTCONTEXT
DOCTPL_HOME = Path(os.getenv("DOCTPL_HOME"))
logging.basicConfig(filename=str(
    DOCTPL_HOME / ".local/doctpl.log"), level=logging.DEBUG)


class Helper:
    def __init__(self) -> None:
        self._read_info = None
        self._files_dir: Path | None = None

    def get_read_info(self):
        if self._read_info is None:
            path = self.file_path("info.json")
            if path.exists():
                with path.open("r", encoding="utf-8") as f:
                    self._read_info = json.load(f)
        return self._read_info

    def get_doc_path(self) -> Path:
        doc = XSCRIPTCONTEXT_.getDocument()
        dir_ = doc.getURL()
        if os.name == "nt":
            return Path(dir_.replace("file:///", ""))
        return Path(dir_.replace("file://", ""))

    def file_path(self, relpah) -> Path:
        return self.get_files_dir() / relpah

    def get_subdoc_url(self, name) -> str:
        return (self.get_files_dir() / f"subdocs/{name}").as_uri()

    def get_files_dir(self) -> Path:
        if self._files_dir is None:
            raise Exception("files_dir was not set")
        return self._files_dir

    def set_files_dir(self, files_dir: Path) -> None:
        self._files_dir = files_dir

    def add_image(self, path, w, h, cur):
        doc = XSCRIPTCONTEXT_.getDocument()
        path = Path(path).absolute()
        if not path.exists():
            print(f"File {path} do not exist")
        img = doc.createInstance('com.sun.star.text.TextGraphicObject')
        img.GraphicURL = path.as_uri()
        img.setPropertyValue('AnchorType', AS_CHARACTER)
        width = w*100
        alfa = width/w
        cur.setString("")
        cur.Text.insertTextContent(cur, img, False)
        height = alfa*h
        img.setSize(Size(width, height))

    def add_subdoc_on_selection(self, path: Path):
        self.replace_selection("{{ replace }}")
        cur = self.find_variable("replace")
        if cur:
            cur.insertDocumentFromURL(path.as_uri(), ())
        logging.info(str(cur))
        

    def replace_selection(self, text):
        desktop = XSCRIPTCONTEXT_.getDesktop()
        model = desktop.getCurrentComponent()
        selection = model.getCurrentSelection()
        selection.getByIndex(0).setString(text)

    def find_variable(self, var):
        doc = XSCRIPTCONTEXT_.getDocument()
        replace = doc.createReplaceDescriptor()
        replace.SearchRegularExpression = True
        reg = r'\{\{\s*$var\s*\}\}'.replace("$var", var)
        replace.SearchString = reg
        selsFound = doc.findAll(replace)
        return doc.findFirst(replace)

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
        doc = XSCRIPTCONTEXT_.getDocument()
        replace = doc.createReplaceDescriptor()
        replace.SearchRegularExpression = True
        reg = r'@(.{1,15}?)\((.{1,100}?)\)'
        replace.SearchString = reg
        selsFound = doc.findAll(replace)
        for i in range(0, selsFound.getCount()):
            selFound = selsFound.getByIndex(i)
            name = selFound.getString().strip()
            res = re.search(reg, name)
            action, args = res.group(1), res.group(2).split(",")
            args = [arg.strip() for arg in args]
            self.replace_action(action, args, selFound)


class Funcs:
    def pos_process(self, files_dir: str):
        helper = Helper()
        helper.set_files_dir(Path(files_dir))
        helper.pos_process()

    def add_doc(self, path: str):
        helper = Helper()
        helper.add_subdoc_on_selection(Path(path))

    def test(self, message):
        desktop = XSCRIPTCONTEXT_.getDesktop()
        model = desktop.getCurrentComponent()
        text = model.Text
        cursor = text.createTextCursor()
        text.insertString(cursor, message, False)


def run_func(base64_str):
    import base64
    json_bytes = base64.b64decode(base64_str)
    json_str = json_bytes.decode('utf-8')
    data = json.loads(json_str)
    funcs = Funcs()
    getattr(funcs, data['func'])(*data['args'], **data['kwargs'])


def open_doctpl():
    import subprocess
    subprocess.Popen(['doctpl'], shell=True)
