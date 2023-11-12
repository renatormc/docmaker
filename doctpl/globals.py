from typing import TYPE_CHECKING, Any
from pathlib import Path
from PIL import Image as PilImage
if TYPE_CHECKING:
    from .renderer import Renderer


def totag(tag: str, *args) -> str:
    args_str = ",".join(args)
    return f"@{tag}({args_str})"


class Image:
    def __init__(self, renderer: 'Renderer') -> None:
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
    def __init__(self, renderer: 'Renderer') -> None:
        self.renderer = renderer

    def __call__(self, template: str,  **kwds: Any) -> Any:
        name = self.renderer.gen_subdoc_name()
        dest = self.renderer.render_files.subdocs_dir / name
        self.renderer.render(template, dest, **kwds)
        return totag("subdoc", name)
