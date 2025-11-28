import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Read DATABASE_URL from environment variable (set by Docker)
# Falls back to localhost for local development
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://papernest_user:papernest_pass@localhost:5432/papernest_db"
)

print(f"🔍 DEBUG: Connecting to database: {DATABASE_URL}")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
