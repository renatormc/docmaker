from . import secretary as sct
from pathlib import Path
from . import globals as gl
import shutil
from typing import Callable
from .render_info import RenderInfo, PicInfo
import json
from doctpl.filters import filters


class RenderFiles:
    def __init__(self, doc_file: Path) -> None:
        self.doc_file = doc_file
        self.render_dir = doc_file.parent / f"{doc_file.stem}_"
        self.render_info = RenderInfo(pics={})

    def init(self, overwrite=False) -> None:
        if overwrite:
            self.clear()
        try:
            self.render_dir.mkdir()
        except FileExistsError:
            pass
        try:
            self.subdocs_dir.mkdir()
        except FileExistsError:
            pass

    @property
    def subdocs_dir(self) -> Path:
        return self.render_dir / "subdocs"
    
    @property
    def render_info_file(self) -> Path:
        return self.render_dir / "info.json"

    def save(self):
        with self.render_info_file.open("w", encoding="utf-8") as f:
            f.write(json.dumps(self.render_info.model_dump(),
                    ensure_ascii=False, indent=4))

    def load_info(self) -> RenderInfo:
        with self.render_info_file.open("r", encoding="utf-8") as f:
            self.render_info = json.load(f)
        return self.render_info

    def clear(self) -> None:
        try:
            shutil.rmtree(self.render_dir)
        except FileNotFoundError:
            pass
        try:
            self.doc_file.unlink()
        except FileNotFoundError:
            pass


class Renderer:

    def __init__(self, model_dir: str | Path) -> None:
        self._render_files: RenderFiles | None = None
        self.model_dir = Path(model_dir)
        self._subdoc_counter = 0
        self._pic_counter = 0
        self.filters: dict[str, Callable] = {}
        self.globals: dict[str, Callable] = {}
    

    def new_engine(self) -> sct.Renderer:
        engine = sct.Renderer()
        engine.environment.globals['image'] = gl.Image(self)
        engine.environment.globals['subdoc'] = gl.SubDoc(self)
        for filter_ in filters:
            engine.environment.filters[filter_.__name__] = filter_
        for name, f in self.filters.items():
            engine.environment.filters[name] = f
        for name, f in self.globals.items():
            engine.environment.globals[name] = f
        return engine

    def gen_subdoc_name(self) -> str:
        self._subdoc_counter += 1
        return f"{self._subdoc_counter}.odt"

    def add_pic(self, path: Path | str, w: int, h: int) -> PicInfo:
        self._pic_counter += 1
        p = PicInfo(w=w, h=h, number=self._pic_counter, path=str(path))
        self.render_files.render_info.pics[str(self._pic_counter)] = p
        return p


    @property
    def render_files(self) -> RenderFiles:
        if self._render_files is None:
            raise Exception("render_files not set")
        return self._render_files

    def filter(self, name: str):
        def decorator(f):
            self.filters[name] = f
            return f
        return decorator

    def function(self, name: str):
        def decorator(f):
            self.globals[name] = f
            return f
        return decorator

    def render(self, template: str, dest: str | Path, **kwargs):
        dest = Path(dest)
        tpl = self.model_dir / template
        engine = self.new_engine()
        result = engine.render(tpl, **kwargs)
        with dest.open('wb') as f:
            f.write(result)

    def pre_render(self, template: str, dest: str | Path, overwrite=False, **kwargs):
        self._render_files = RenderFiles(dest)
        self.render_files.init(overwrite=overwrite)
        self.render(template, dest, **kwargs)
        self.render_files.save()
