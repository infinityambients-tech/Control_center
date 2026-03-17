from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "Control Core API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    SECRET_KEY: str = "your-super-secret-key-change-it-in-prod"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    DATABASE_URL: str = "postgresql://postgres:postgres@localhost/control_core"

    # Redis for Celery / cache
    REDIS_URL: str = "redis://localhost:6379/0"

    # Email Configuration
    SMTP_SERVER: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    EMAIL_FROM: str = "noreply@control-center.pl"
    FRONTEND_URL: str = "http://localhost:5173"

    # Updates (GitHub Releases): "owner/repo" (can also be stored in DB setting `github_repo`)
    GITHUB_REPO: str | None = None
    # Optional token (PAT or GitHub Actions token) to avoid rate limits / support private repos.
    # Can also be stored in DB setting `github_token`.
    GITHUB_TOKEN: str | None = None

    # Verification settings
    VERIFICATION_TOKEN_EXPIRE_HOURS: int = 24

    # Project Aggregation
    SYNC_INTERVAL_MINUTES: int = 5

    ALLOWED_HOSTS: List[str] = ["*"]

    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_file=".env",
        extra="ignore",
    )


settings = Settings()
