from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://vanishjain@localhost/papernest_db"
    SECRET_KEY: str = "dev-secret-key-change-in-production"
    
    class Config:
        env_file = ".env"

settings = Settings()