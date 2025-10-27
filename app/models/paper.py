from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.sql import func
import enum
from app.db.database import Base

class StatusEnum(str, enum.Enum):
    TO_READ = "to_read"
    READING = "reading"
    DONE = "done"

class PriorityEnum(str, enum.Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class Paper(Base):
    __tablename__ = "papers"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    authors = Column(String)
    status = Column(Enum(StatusEnum), default=StatusEnum.TO_READ)
    priority = Column(Enum(PriorityEnum), default=PriorityEnum.MEDIUM)
    categories = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())