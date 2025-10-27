from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.models.paper import Paper
from app.schemas.paper import PaperCreate, PaperResponse

router = APIRouter(prefix="/papers", tags=["papers"])

@router.post("/", response_model=PaperResponse, status_code=status.HTTP_201_CREATED)
def create_paper(paper: PaperCreate, db: Session = Depends(get_db)):
    """Create a new research paper entry"""
    db_paper = Paper(**paper.model_dump())
    db.add(db_paper)
    db.commit()
    db.refresh(db_paper)
    return db_paper

@router.get("/", response_model=List[PaperResponse])
def get_papers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all papers with pagination"""
    papers = db.query(Paper).offset(skip).limit(limit).all()
    return papers

@router.get("/{paper_id}", response_model=PaperResponse)
def get_paper(paper_id: int, db: Session = Depends(get_db)):
    """Get a specific paper by ID"""
    paper = db.query(Paper).filter(Paper.id == paper_id).first()
    if not paper:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Paper with id {paper_id} not found"
        )
    return paper