from fastapi import Header, HTTPException, status, Depends
from sqlalchemy.orm import Session

from app.core.sessions import get_session_user
from app.db.database import get_db
from app.models.user import User

def get_current_user(
    session_id: str = Header(None, alias="X-Session-ID"),
    db: Session = Depends(get_db)
) -> User:
    """
    Dependency to get current authenticated user from session.
    """
    if not session_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    
    user_id = get_session_user(session_id)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired session"
        )
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    return user
