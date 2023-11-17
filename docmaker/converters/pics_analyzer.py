from docmaker.gui.widgets.types import ValidationError
import re
from typing import TypedDict, Optional
from pathlib import Path


class AnalyzedPicInfo(TypedDict):
    obj_name: str
    alias: str
    obj_number: str
    pic_seq: str


class NameAnalyzer:
    def __init__(self):
        self.reg = re.compile(r'((^[A-Za-z]+)(\d+))(?:[\d\.\-]+)?(?:_(\d+))?$')

    def analise_name(self, name) -> Optional[AnalyzedPicInfo]:
        res = self.reg.search(name)
        if not res:
            return None
        ret: AnalyzedPicInfo = {
            'obj_name': res.group(1),
            'alias': res.group(2),
            'obj_number': res.group(3),
            'pic_seq': res.group(4)
        }
        if ret['obj_number'] is not None:
            return ret


class ObjectPics(TypedDict):
    name: str
    report_name: str
    number: int
    pics: list[str]
    pics_files: list[str]


class PicsAnalyzer:
    def __init__(self, subfolder="", prefix="Vestígios") -> None:
        self.subfolder = subfolder
        self.prefix = prefix

    def __call__(self,  folder: str | Path) -> list[ObjectPics]:
        directory = Path(folder) / self.subfolder

        objects: dict[str, ObjectPics] = {}
        if not directory.is_dir():
            return []
        analyzer = NameAnalyzer()
        for entry in directory.iterdir():
            if entry.name.startswith("_"):
                continue
            res = analyzer.analise_name(entry.stem)
            if not res:
                continue
            obj = res['obj_name']
            try:
                objects[obj]['pics'].append(str(entry))
            except KeyError:
                objects[obj] = {'name': obj, 'report_name': f"Vestígio {res['obj_number']}", 'number': int(
                    res['obj_number']), 'pics': [str(entry)], 'pics_files': []}
            objects[obj]['pics_files'].append(entry.name)
        items: list[ObjectPics] = []
        for key, value in objects.items():
            objects[key]['pics'].sort()
            items.append({
                'name': key,
                'report_name': f"{self.prefix} {value['number']}",
                'number': value['number'],
                'pics': value['pics'],
                'pics_files': value['pics_files']
            })
        items.sort(key=lambda x: x['number'])
        return items
