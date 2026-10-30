from pydantic import BaseModel
from typing import List

class ActionItem(BaseModel):
    type: str
    details: str

class ActionItemList(BaseModel):
    actions: List[ActionItem]