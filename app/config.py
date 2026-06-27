import os
from functools import lru_cache
from dotenv import load_dotenv

load_dotenv()


class Settings:
    google_api_key: str | None = os.getenv("GOOGLE_API_KEY")
    db_user: str = os.getenv("DB_USER", "root")
    db_password: str = os.getenv("DB_PASSWORD", "")
    db_host: str = os.getenv("DB_HOST", "localhost")
    db_port: str = os.getenv("DB_PORT", "3306")
    db_name: str = os.getenv("DB_NAME", "text_to_sql")
    allowed_origins: list[str] = [
        origin.strip()
        for origin in os.getenv(
            "ALLOWED_ORIGINS",
            "http://localhost:8501,http://127.0.0.1:8501,http://localhost:8000,http://127.0.0.1:8000,http://localhost:5173,http://localhost:8080",
        ).split(",")
        if origin.strip()
    ]


@lru_cache
def get_settings() -> Settings:
    return Settings()
