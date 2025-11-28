from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://papernest_user:papernest_pass@localhost:5432/papernest_db"
    SECRET_KEY: str = "dev-secret-key-change-in-production"
    
    model_config = {
        "env_file": ".env",
        "case_sensitive": False,
        "extra": "ignore"
    }

settings = Settings()
