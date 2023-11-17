from pathlib import Path
import jinja2
from typing import Callable
from docmaker.doc_handler.filters import filters
from docmaker.doc_handler.jinja_env_functions import global_functions


def make_jinja_env(custom_filters: dict[str, Callable],
                   custom_global_functions: dict[str, Callable],
                   folder_templates: str | Path | None = None) -> jinja2.Environment:

    if folder_templates is not None:
        jinja_env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(folder_templates))
    else:
        jinja_env = jinja2.Environment()
    for filter_ in filters:
        jinja_env.filters[filter_.__name__] = filter_
    for function_ in global_functions:
        jinja_env.globals[function_.__name__] = function_
    for name, f in custom_filters.items():
        jinja_env.filters[name] = f
    for name, f in custom_global_functions.items():
        jinja_env.globals[name] = f
    return jinja_env
