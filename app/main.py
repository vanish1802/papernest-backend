from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.database import engine, Base

# Create database tables (none yet, but ready for tomorrow)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="PaperNest API",
    description="Research Paper Management System",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Welcome to PaperNest!", "database": "connected"}

@app.get("/health")
def health():
    return {"status": "healthy", "database": "PostgreSQL"}