# app/config.py
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database
    database_url: str = "sqlite+aiosqlite:///./user_service.db"

    # JWT Secret
    secret_key: str = "your-secret-key-change-this-in-production-use-openssl-rand-hex-32"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 1440  # 24 hours

    # API
    api_title: str = "User Microservice API"
    api_version: str = "1.0.0"
    api_prefix: str = "/api/v1"

    # CORS
    cors_origins: list[str] = ["http://localhost:3000", "http://localhost:8000"]

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()

