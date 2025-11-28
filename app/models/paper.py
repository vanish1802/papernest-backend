from sqlalchemy import Column, Integer, String, Enum, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from app.db.database import Base

class StatusEnum(str, enum.Enum):
    TO_READ = "TO_READ"
    READING = "READING"
    DONE = "DONE"

class PriorityEnum(str, enum.Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"

class Paper(Base):
    __tablename__ = "papers"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    authors = Column(String, nullable=True)
    status = Column(Enum(StatusEnum), default=StatusEnum.TO_READ)
    priority = Column(Enum(PriorityEnum), default=PriorityEnum.MEDIUM)
    categories = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # NEW: Add these two columns
    paper_text = Column(Text, nullable=True)  # Store paper content
    summary = Column(Text, nullable=True)     # Store AI summary
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    user = relationship("User", back_populates="papers")
