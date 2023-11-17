from typing import TYPE_CHECKING, Any
from pathlib import Path
from PIL import Image as PilImage
from docmaker.custom_types import ContextType
if TYPE_CHECKING:
    from docmaker.doc_handler.odt_handler import OdtHandler


def totag(tag: str, *args) -> str:
    args_str = ",".join(args)
    return f"@{tag}({args_str})"


class Image:
    def __init__(self, renderer: 'OdtHandler') -> None:
        self.renderer = renderer

    def __call__(self, path: Path | str | None, w: int | None = None, h: int | None = None) -> Any:
        if not path:
            return ""
        if w is None and h is None:
            raise Exception("w or h is required")
        img = PilImage.open(path)
        alfa = img.height/img.width
        if h is None:
            h = int(alfa*w)
        if w is None:
            w = int(h/alfa)
        path = Path(path)
        info = self.renderer.add_pic(path, w, h)
        return totag("image", str(info.number))


class SubDoc:
    def __init__(self, renderer: 'OdtHandler') -> None:
        self.renderer = renderer

    def __call__(self, template: str,  **context: ContextType) -> Any:
        name = self.renderer.render_subdoc(template, context)
        return totag("subdoc", name)
