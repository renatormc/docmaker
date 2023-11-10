from com.sun.star.text.TextContentAnchorType import AS_CHARACTER
from com.sun.star.awt import Size
from pathlib import Path
import re
import logging
import os
import json
from pathlib import Path


class Helper:
    def __init__(self) -> None:
        self.doc = XSCRIPTCONTEXT.getDocument()
        filename = str(self.file_path("log.log"))
        logging.basicConfig(filename=str(self.file_path(
            "log.log")), encoding='utf-8', level=logging.DEBUG)
        logging.info("Teste")
        self.render_info = self.read_info()

    def read_info(self):
        path = self.file_path("info.json")
        logging.info(str(path))
        if path.exists():
            with path.open("r", encoding="utf-8") as f:
                data = json.load(f)
            return data

    def file_path(self, relpath: str) -> Path:
        dir_ = self.doc.getURL()
        if os.name == "nt":
            path = Path(dir_.replace("file:///", "")).parent / relpath
        else:
            path = Path(dir_.replace("file://", "")).parent / relpath
        return path

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
