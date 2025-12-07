import logging
from pydantic import AnyHttpUrl, EmailStr
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "Leads Service"
    DATABASE_URL: str = "sqlite:///leads.db"
    UPLOAD_DIR: str = "./uploads"

    # Email (optional)
    SMTP_HOST: Optional[str] = None
    SMTP_PORT: Optional[int] = None
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    FROM_EMAIL: Optional[EmailStr] = None
    ATTORNEY_EMAIL: Optional[EmailStr] = None

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    class Config:
        env_file = ".env"

settings = Settings()
