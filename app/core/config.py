from pydantic_settings import BaseSettings
import os
from functools import lru_cache

class Settings(BaseSettings):
    """Application settings."""
    PROJECT_NAME: str = "Mind Mirror"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://jamesguy@localhost/mindmirror")
    
    # OpenAI
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    
    class Config:
        case_sensitive = True
        env_file = ".env"

@lru_cache()
def get_settings() -> Settings:
    """Get cached settings."""
    return Settings()
