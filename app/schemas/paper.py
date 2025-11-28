from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.models.paper import StatusEnum, PriorityEnum

class PaperCreate(BaseModel):
    title: str
    authors: Optional[str] = None
    status: Optional[StatusEnum] = StatusEnum.TO_READ
    priority: Optional[PriorityEnum] = PriorityEnum.MEDIUM
    categories: Optional[str] = None
    paper_text: Optional[str] = None  # NEW: For summarization input

class PaperUpdate(BaseModel):
    title: Optional[str] = None
    authors: Optional[str] = None
    status: Optional[StatusEnum] = None
    priority: Optional[PriorityEnum] = None
    categories: Optional[str] = None
    paper_text: Optional[str] = None  # NEW

class PaperResponse(BaseModel):
    id: int
    title: str
    authors: Optional[str]
    status: StatusEnum
    priority: PriorityEnum
    categories: Optional[str]
    user_id: int
    paper_text: Optional[str]  # NEW
    summary: Optional[str]     # NEW
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True

# NEW: Schema for summarization response
class SummarizationResponse(BaseModel):
    paper_id: int
    summary: str
