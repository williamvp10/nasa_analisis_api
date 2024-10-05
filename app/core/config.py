# app/core/config.py

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Nasa Analisis API"
    DATABASE_URL: str

    class Config:
        env_file = ".env"

settings = Settings()
