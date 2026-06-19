from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import AnyHttpUrl, field_validator

class Settings(BaseSettings):
    ENVIRONMENT: str = "development"
    SECRET_KEY: str | None = None
    TMDB_API_KEY: str | None = None
    
    # CORS Origins parses from string list format or uses defaults
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173", "https://insight-ai.vercel.app"]

    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
