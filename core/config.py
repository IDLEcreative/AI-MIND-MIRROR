from pydantic import BaseSettings, Field
from pathlib import Path

class Settings(BaseSettings):
    DATABASE_URL: str = Field(..., env="DATABASE_URL")
    OPENAI_API_KEY: str = Field(..., env="OPENAI_API_KEY")
    SECRET_KEY: str = Field(..., env="SECRET_KEY")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 1 week

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
