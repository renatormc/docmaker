from tinydb import TinyDB, Query
from tinydb.storages import JSONStorage
from tinydb_serialization import SerializationMiddleware
from tinydb_serialization.serializers import DateTimeSerializer
from docmaker.config import get_config
from datetime import datetime
from typing import TypedDict
from docmaker.custom_types import ContextType
from pathlib import Path
from docmaker.helpers import read_json_file, write_json_file

serialization = SerializationMiddleware(JSONStorage)
serialization = SerializationMiddleware(JSONStorage)
serialization.register_serializer(DateTimeSerializer(), 'TinyDate')


_db: TinyDB | None = None

def get_db() -> TinyDB:
    global _db
    if _db is None:
        raise Exception("db was not initialized")
    return _db

def connect(path: Path) -> None:
    global _db
    _db = TinyDB(path, storage=serialization)


def save_last_context(model_name: str, context: ContextType) -> None:
    db = get_db()
    updated_at = datetime.now().timestamp()
    Record = Query()
    cond = (Record.id == "last_context") & (Record.model_name == model_name)
    if db.contains(cond):
        db.update({'context': context, "updated_at": updated_at}, cond)
    else:
        db.insert(
            {'id': 'last_context', 'model_name': model_name, 'context': context, "updated_at": updated_at})


def get_last_context_by_model(model_name: str) -> ContextType:
    db = get_db()
    Record = Query()
    cond = (Record.id == "last_context") & (Record.model_name == model_name)
    res = db.search(cond)
    if len(res) == 0:
        return {}
    return res[0]['context']


class LastContext(TypedDict):
    id: str
    model_name: str
    context: ContextType


def get_last_context() -> LastContext | None:
    db = get_db()
    Record = Query()
    regs = sorted(db.search(Record.id == "last_context"),
                  key=lambda x: x['updated_at'])
    if len(regs) == 0:
        return None
    return regs[-1]


def save_last_context_dev(context: ContextType, full: bool) -> None:
    cf = get_config()
    name = "last_context_dev_full.json" if full else "last_context_dev_filled.json"
    write_json_file(cf.local_folder / name, context)
   


def get_last_filled_context(full: bool) -> ContextType:
    cf = get_config()
    name = "last_context_dev_full.json" if full else "last_context_dev_filled.json"
    try:
        return read_json_file(cf.local_folder / name)
    except FileNotFoundError:
        return {}
