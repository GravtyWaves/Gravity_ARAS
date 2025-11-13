"""
ARAS Microservice Configuration
Environment-based settings using Pydantic

Built by Elite Team - Security Specialist (PhD in Cybersecurity)
"""

import secrets
from typing import List, Union

from pydantic import AnyHttpUrl, field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application settings with environment variable support.

    All sensitive data is loaded from environment variables.
    Never hardcode secrets in code.
    """

    # API Configuration
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days

    # Server Configuration
    SERVER_NAME: str = "ARAS Microservice"
    SERVER_HOST: AnyHttpUrl = "http://localhost"
    PORT: int = 8000
    DEBUG: bool = True

    # CORS Configuration
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = [
        "http://localhost:3000",  # React dev server
        "http://localhost:8000",  # FastAPI
    ]

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # Database Configuration (DB-agnostic)
    DATABASE_URL: str = "postgresql+asyncpg://user:password@localhost/aras_db"
    DATABASE_POOL_SIZE: int = 20
    DATABASE_MAX_OVERFLOW: int = 30

    # Redis Configuration
    REDIS_URL: str = "redis://localhost:6379"
    REDIS_CACHE_TTL: int = 3600  # 1 hour

    # Security Configuration
    ALLOWED_HOSTS: List[str] = ["localhost", "127.0.0.1"]

    # NLP Configuration
    SPACY_MODEL: str = "en_core_web_sm"
    HAZM_MODEL: str = "hazm"

    # News Sources Configuration
    NEWS_SOURCES: List[str] = [
        "https://rss.cnn.com/rss/edition.rss",
        "https://feeds.bbci.co.uk/news/rss.xml",
        "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml",
    ]

    # Celery Configuration (for async tasks)
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"

    # Logging Configuration
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # Feature Flags
    ENABLE_ANALYTICS: bool = True
    ENABLE_TREND_DETECTION: bool = True
    ENABLE_SENTIMENT_ANALYSIS: bool = True

    class Config:
        env_file = ".env"
        case_sensitive = True


# Create global settings instance
settings = Settings()
