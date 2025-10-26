from fastapi import FastAPI

app = FastAPI(
    title="PaperNest API",
    description="Research Paper Management System",
    version="1.0.0"
)

@app.get("/")
def home():
    return {"message": "Welcome to PaperNest!"}

@app.get("/health")
def health():
    return {"status": "healthy"}