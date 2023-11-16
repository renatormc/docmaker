from pydantic import BaseModel

class PicInfo(BaseModel):
    path: str
    number: int
    w: int
    h: int

class RenderInfo(BaseModel):
    doc_file: str
    pics: dict[str, PicInfo]