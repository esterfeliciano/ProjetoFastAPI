# Configurações do bd
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import create_engine
from sqlalchemy.orm import Session


class DatabaseSettings(BaseSettings):
    DATABASE_URL: str  # <--- Adicione esta linha

    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8', extra='ignore'
    )


engine = create_engine(DatabaseSettings().DATABASE_URL)


def get_session():
    with Session(engine) as session:
        yield sessions