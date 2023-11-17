from . import secretary as sct
from pathlib import Path
from . import globals as gl
import shutil
from typing import Callable, TYPE_CHECKING, Union, Optional
from .render_info import RenderInfo, PicInfo
import json
from docmaker.doc_handler.filters import filters
from docmaker.doc_handler.jinja_env_functions import global_functions
from docmaker.custom_types import ContextType
from .helpers import get_files_dir_path
if TYPE_CHECKING:
    from docmaker.docmodel import DocModel


class RenderOutput:
    def __init__(self, doc_file: Path) -> None:
        self.doc_file = Path(doc_file).absolute()
        self.files_dir = get_files_dir_path(self.doc_file)
        self.render_info = RenderInfo(pics={}, doc_file=str(self.doc_file))

    def init(self, overwrite=False) -> None:
        if overwrite:
            self.clear()
        try:
            self.files_dir.mkdir()
        except FileExistsError:
            pass
        try:
            self.subdocs_dir.mkdir()
        except FileExistsError:
            pass

    @property
    def subdocs_dir(self) -> Path:
        return self.files_dir / "subdocs"

    @property
    def render_info_file(self) -> Path:
        return self.files_dir / "info.json"

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
            shutil.rmtree(self.files_dir)
        except FileNotFoundError:
            pass
        try:
            self.doc_file.unlink()
        except FileNotFoundError:
            pass


class OdtHandler:

    def __init__(self, docmodel: 'DocModel') -> None:
        self._render_files: RenderOutput | None = None
        self.docmodel = docmodel
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
        for function_ in global_functions:
            engine.environment.globals[function_.__name__] = function_
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
    def render_files(self) -> RenderOutput:
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

    def render_odt(self, template: str, dest: str | Path, context: ContextType):
        dest = Path(dest)
        tpl = self.docmodel.templates_folder / template
        engine = self.new_engine()
        result = engine.render(tpl, **context)
        with dest.open('wb') as f:
            f.write(result)

    def render_subdoc(self, template: str, context: ContextType) -> str:
        name = self.gen_subdoc_name()
        dest = self.render_files.subdocs_dir / name
        self.render_odt(template, dest, context)
        return name


    def render(self, template: str, context: ContextType, dest_file: Union[Path, str]) -> Optional[Path]:
        self._render_files = RenderOutput(Path(dest_file))
        self.render_files.init(overwrite=True)
        self.render_odt(template, dest_file, context)
        self.render_files.save()
        return self.render_files.doc_file
