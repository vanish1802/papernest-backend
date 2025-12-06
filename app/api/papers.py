from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.models.paper import Paper 
from app.models.user import User
from app.schemas.paper import PaperCreate, PaperResponse, PaperUpdate, SummarizationResponse
from app.core.dependencies import get_current_user
from app.core.summarizer import summarize_text

router = APIRouter(prefix="/papers", tags=["papers"])


@router.post("/", response_model=PaperResponse, status_code=status.HTTP_201_CREATED)
def create_paper(
    paper: PaperCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  # ← ADDED THIS
):
    """Create a new research paper entry"""
    db_paper = Paper(
        title=paper.title,
        authors=paper.authors,
        status=paper.status,
        priority=paper.priority,
        categories=paper.categories,
        paper_text=paper.paper_text,
        user_id=current_user.id  # ← ADDED THIS - CRITICAL!
    )
    db.add(db_paper)
    db.commit()
    db.refresh(db_paper)
    return db_paper


@router.get("/", response_model=List[PaperResponse])
def get_papers(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  # ← ADDED AUTH
):
    """Get all papers for current user with pagination"""
    papers = db.query(Paper).filter(
        Paper.user_id == current_user.id  # ← ADDED - Only user's papers
    ).offset(skip).limit(limit).all()
    return papers


@router.get("/{paper_id}", response_model=PaperResponse)
def get_paper(
    paper_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  # ← ADDED AUTH
):
    """Get a specific paper by ID"""
    paper = db.query(Paper).filter(
        Paper.id == paper_id,
        Paper.user_id == current_user.id  # ← ADDED - Security check
    ).first()
    if not paper:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Paper with id {paper_id} not found"
        )
    return paper


@router.patch("/{paper_id}", response_model=PaperResponse)
def update_paper(
    paper_id: int,
    paper_update: PaperUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  # ← ADDED AUTH
):
    """Update a paper's details"""
    paper = db.query(Paper).filter(
        Paper.id == paper_id,
        Paper.user_id == current_user.id  # ← ADDED - Security check
    ).first()
    if not paper:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Paper with id {paper_id} not found"
        )
    
    update_data = paper_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(paper, field, value)
    
    db.commit()
    db.refresh(paper)
    return paper


@router.delete("/{paper_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_paper(
    paper_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  # ← ADDED AUTH
):
    """Delete a paper"""
    paper = db.query(Paper).filter(
        Paper.id == paper_id,
        Paper.user_id == current_user.id  # ← ADDED - Security check
    ).first()
    if not paper:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Paper with id {paper_id} not found"
        )
    
    db.delete(paper)
    db.commit()
    return None


@router.post("/{paper_id}/summarize", response_model=SummarizationResponse)
async def summarize_paper(
    paper_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Generate AI summary for a paper.
    Paper must have paper_text field populated.
    """
    # Get paper
    paper = db.query(Paper).filter(
        Paper.id == paper_id,
        Paper.user_id == current_user.id
    ).first()
    
    if not paper:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Paper not found"
        )
    
    # Check if paper has text
    if not paper.paper_text:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Paper has no text content. Add paper_text first."
        )
    
    # Generate summary
    summary = summarize_text(paper.paper_text)
    
    # Save summary to database
    paper.summary = summary
    db.commit()
    db.refresh(paper)
    
    return SummarizationResponse(
        paper_id=paper.id,
        summary=summary
    )


from fastapi import File, UploadFile, Form
from app.core.pdf_utils import extract_text_from_pdf
from app.core.chat import chat_with_paper

@router.post("/upload", response_model=PaperResponse, status_code=status.HTTP_201_CREATED)
async def upload_paper(
    file: UploadFile = File(...),
    title: str = Form(...),
    authors: str = Form(None),
    status: str = Form("TO_READ"),
    priority: str = Form("MEDIUM"),
    categories: str = Form(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Upload a PDF paper, extract text, and save it"""
    # Extract text from PDF
    try:
        text_content = await extract_text_from_pdf(file)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to process PDF: {str(e)}")
    
    # Create paper entry
    db_paper = Paper(
        title=title,
        authors=authors,
        status=status,
        priority=priority,
        categories=categories,
        paper_text=text_content,
        user_id=current_user.id
    )
    db.add(db_paper)
    db.commit()
    db.refresh(db_paper)
    return db_paper


@router.post("/{paper_id}/chat")
async def chat_with_paper_endpoint(
    paper_id: int,
    query: str = Form(...),  # Using Form to keep it simple, or body Pydantic model
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Chat with a specific paper"""
    paper = db.query(Paper).filter(
        Paper.id == paper_id,
        Paper.user_id == current_user.id
    ).first()
    
    if not paper:
        raise HTTPException(status_code=404, detail="Paper not found")
        
    if not paper.paper_text:
        raise HTTPException(status_code=400, detail="Paper has no text content")
        
    response = chat_with_paper(paper.paper_text, query)
    return {"response": response}
