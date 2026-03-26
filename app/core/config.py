import os
from dotenv import load_dotenv

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    load_dotenv()
    POSTGRES_USER: str | None = os.environ.get("POSTGRES_USER")
    POSTGRES_PASSWORD: str | None = os.environ.get("POSTGRES_PASSWORD")
    POSTGRES_HOST: str | None = os.environ.get("POSTGRES_HOST")
    POSTGRES_PORT: str | None = os.environ.get("POSTGRES_PORT")
    POSTGRES_DB: str | None = os.environ.get("POSTGRES_DB")

    ECHO: bool = True

    DB_URL: str = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"


settings = Settings()
