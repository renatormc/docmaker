from typing import Any, TypedDict
from doctpl.custom_types import ConverterType
from doctpl.gui.widgets.types import ValidationError
# from database import repo

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

def get_list(choices: list|str, model_name: str) -> list[ChoicesType]:
    if isinstance(choices, list):
        return [to_list_item(item) for item in choices]
    elif isinstance(choices, str):
        return [{"key": item.key, "data": item.data} for item in repo.get_list(model_name, choices)]
    return []
