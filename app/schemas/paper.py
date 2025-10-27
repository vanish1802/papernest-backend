from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.models.paper import StatusEnum, PriorityEnum

class PaperBase(BaseModel):
    title: str
    authors: Optional[str] = None
    status: StatusEnum = StatusEnum.TO_READ
    priority: PriorityEnum = PriorityEnum.MEDIUM
    categories: Optional[str] = None

class PaperCreate(PaperBase):
    pass

class PaperUpdate(BaseModel):
    title: Optional[str] = None
    authors: Optional[str] = None
    status: Optional[StatusEnum] = None
    priority: Optional[PriorityEnum] = None
    categories: Optional[str] = None

class PaperResponse(PaperBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True