# Configurações do bd
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

class DatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8'
    )

engine = create_engine(DatabaseSettings().DATABASE_URL)

def get_session():
    with Session(engine) as session:
        yield session