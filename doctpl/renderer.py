from . import secretary as sct
from pathlib import Path
from . import globals as gl
import shutil
from typing import Callable
from .render_info import RenderInfo, PicInfo
import json

class Renderer:

    def __init__(self, model_dir: str | Path) -> None:
        self._pre_render_dir: Path | None = None
        self.model_dir = Path(model_dir)
        self._subdoc_counter = 0
        self._pic_counter = 0
        self.filters: dict[str, Callable] = {}
        self.globals: dict[str, Callable] = {}
        self.render_info: RenderInfo = RenderInfo(pics={})

    def new_engine(self) -> sct.Renderer:
        engine = sct.Renderer()
        engine.environment.globals['image'] = gl.Image(self)
        engine.environment.globals['subdoc'] = gl.SubDoc(self)
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
        self.render_info.pics[str(self._pic_counter)] = p
        return p
    
    def save_info(self):
        p = self.pre_render_dir / "info.json"
        with p.open("w", encoding="utf-8") as f:
            f.write(json.dumps(self.render_info.model_dump(), ensure_ascii=False, indent=4))

    @property
    def pre_render_dir(self) -> Path:
        if self._pre_render_dir is None:
            raise Exception("pre_render_dir not set")
        return self._pre_render_dir

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
        self._pre_render_dir = Path(dest)
        if overwrite:
            try:
                shutil.rmtree(self._pre_render_dir)
            except FileNotFoundError:
                pass
        self._pre_render_dir.mkdir()
        (self._pre_render_dir / "subdocs").mkdir()
        self.render(template, self._pre_render_dir / "main.odt", **kwargs)
        self.save_info()
