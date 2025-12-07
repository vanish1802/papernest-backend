from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    # Limit password to 72 bytes (bcrypt limit)
    # We encode to utf-8, extract first 72 bytes, and decode back (ignoring split chars)
    # This ensures we pass a valid string that results in <=72 bytes
    truncated = password.encode('utf-8')[:72].decode('utf-8', 'ignore')
    return pwd_context.hash(truncated)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    truncated = plain_password.encode('utf-8')[:72].decode('utf-8', 'ignore')
    return pwd_context.verify(truncated, hashed_password) 