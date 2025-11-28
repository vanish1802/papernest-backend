from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

from app.db.database import engine, Base
from app.api import papers as papers_router
from app.api import auth as auth_router

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="PaperNest API", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Custom OpenAPI schema to add X-Session-ID security
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title="PaperNest API",
        version="1.0.0",
        description="Research Paper Management System with AI Summarization",
        routes=app.routes,
    )
    
    # Add X-Session-ID security scheme
    openapi_schema["components"]["securitySchemes"] = {
        "SessionAuth": {
            "type": "apiKey",
            "in": "header",
            "name": "X-Session-ID"
        }
    }
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# Routers
app.include_router(auth_router.router)
app.include_router(papers_router.router)

@app.get("/")
def home():
    return {"message": "Welcome to PaperNest API - Research Paper Management System"}

@app.get("/health")
def health():
    return {"status": "healthy"}
