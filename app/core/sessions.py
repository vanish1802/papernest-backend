# Centralized in-memory session storage
sessions = {}

def create_session(user_id: int) -> str:
    """Create new session, return session_id"""
    import secrets
    session_id = secrets.token_urlsafe(32)
    sessions[session_id] = user_id
    return session_id

def get_session_user(session_id: str) -> int:
    """Get user_id from session, returns None if not found"""
    return sessions.get(session_id)

def delete_session(session_id: str) -> bool:
    """Delete session, returns True if existed"""
    return sessions.pop(session_id, None) is not None
