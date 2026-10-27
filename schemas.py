from typing import List, Optional
from pydantic import BaseModel, Field


class ActionItem(BaseModel):
    task: str = Field(
        ...,
        description="Clear description of the action item or task to be completed."
    )
    assignee: Optional[str] = Field(
        default="Unassigned",
        description="Name of the person responsible for executing the task, or 'Unassigned' if unspecified."
    )
    due_date: Optional[str] = Field(
        default=None,
        description="Mentioned deadline or timeframe (e.g., '2026-11-01', 'End of day Friday', or null)."
    )
    priority: str = Field(
        default="medium",
        description="Priority level of the task: must be 'high', 'medium', or 'low'."
    )


class ActionItemList(BaseModel):
    actions: List[ActionItem] = Field(
        default_factory=list,
        description="List of all extracted action items from the audio transcript."
    )