from tinydb import TinyDB, Query
import config
import json
from datetime import datetime
from typing import TypedDict
from doctpl.custom_types import Context

db = TinyDB(config.LOCAL_FOLDER / "db.json")


def save_last_context(model_name: str, context: Context) -> None:
    updated_at = datetime.now().timestamp()
    Record = Query()
    cond = (Record.id == "last_context") & (Record.model_name == model_name)
    if db.contains(cond):
        db.update({'context': context, "updated_at": updated_at}, cond)
    else:
        db.insert(
            {'id': 'last_context', 'model_name': model_name, 'context': context, "updated_at": updated_at})


def get_last_context_by_model(model_name: str) -> Context:
    Record = Query()
    cond = (Record.id == "last_context") & (Record.model_name == model_name)
    res = db.search(cond)
    if len(res) == 0:
        return {}
    return res[0]['context']


class LastContext(TypedDict):
    id: str
    model_name: str
    context: Context


def get_last_context() -> LastContext | None:
    Record = Query()
    regs = sorted(db.search(Record.id == "last_context"),
                  key=lambda x: x['updated_at'])
    if len(regs) == 0:
        return None
    return regs[-1]


def save_last_context_dev(context: Context, full: bool) -> None:
    name = "last_context_dev_full.json" if full else "last_context_dev_filled.json"
    with (config.LOCAL_FOLDER / name).open("w", encoding="utf8") as f:
        f.write(json.dumps(context, ensure_ascii=False, indent=4))


def get_last_filled_context(full: bool) -> Context:
    name = "last_context_dev_full.json" if full else "last_context_dev_filled.json"
    try:
        with (config.LOCAL_FOLDER / name).open("r", encoding="utf8") as f:
            context = json.load(f)
        return context
    except FileNotFoundError:
        return {}
