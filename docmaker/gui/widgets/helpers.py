from typing import Any, TypedDict
from docmaker.custom_types import ConverterType
from docmaker.gui.widgets.types import ValidationError
from pathlib import Path
import json
from docmaker.helpers import read_json_file

def apply_converter(value, converter: ConverterType) -> Any:
    try:
        return converter(value)
    except Exception as e:
        raise ValidationError(f"Valor inválido")

class ChoicesType(TypedDict):
    key: str
    data: Any

def to_list_item(value: str|ChoicesType) -> ChoicesType:
    if isinstance(value, str):
        return {'key': value, 'data': value}
    return value

def get_list(choices: list|str, lists_folder: Path) -> list[ChoicesType]:
    if isinstance(choices, list):
        return [to_list_item(item) for item in choices]
    elif isinstance(choices, str):
        try:
            data = read_json_file(lists_folder / f"{choices}.json")
            # with (lists_folder / f"{choices}.json").open("r", encoding="utf-8") as f:
            #     data = json.load(f)
            return [{"key": item['key'], "data": item['value']} for item in data]
        except FileNotFoundError:
            return []
    return []
