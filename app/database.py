import urllib.parse
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from app.config import get_settings


def get_engine() -> Engine:
    settings = get_settings()
    encoded_password = urllib.parse.quote_plus(settings.db_password)
    url = (
        f"mysql+mysqlconnector://{settings.db_user}:{encoded_password}"
        f"@{settings.db_host}:{settings.db_port}/{settings.db_name}"
    )
    return create_engine(url, pool_pre_ping=True)
