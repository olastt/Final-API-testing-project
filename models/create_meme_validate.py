from typing import List
from pydantic import BaseModel


class Info(BaseModel):
    colors: List[str]


class MemeResponse(BaseModel):
    id: int
    info: Info
    tags: List[str]
    text: str
    updated_by: str
    url: str