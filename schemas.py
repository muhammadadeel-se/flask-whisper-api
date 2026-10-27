from pydantic import BaseModel
from typing import List, Optional

class ActionItem(BaseModel):
    type: str
    details: str

class ActionItemList(BaseModel):
    actions: List[ActionItem]