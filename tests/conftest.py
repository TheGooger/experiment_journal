import pytest
import asyncio
import os
from dotenv import load_dotenv
from typing import AsyncGenerator, Generator
from fastapi.testclient import TestClient

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.pool import NullPool

from app.db.models.base import Base
from app.db.session import get_db 
from main import app


load_dotenv()
POSTGRES_USER = os.environ.get("POSTGRES_USER")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
POSTGRES_HOST = os.environ.get("POSTGRES_HOST")
POSTGRES_PORT = os.environ.get("POSTGRES_PORT")
POSTGRES_DB = "test_db"
# Тестовая БД
DATABASE_URL = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"


@pytest.fixture(scope="session")
def event_loop():
    """Создает event loop для всех тестов"""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def engine():
    """Создает движок для тестовой БД"""
    engine = create_async_engine(DATABASE_URL, poolclass=NullPool)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()


@pytest.fixture
async def db_session(engine) -> AsyncGenerator[AsyncSession, None]:
    """Создает сессию в транзакции, которая откатывается после теста"""
    async with engine.connect() as connection:
        # Начинаем транзакцию
        await connection.begin()
        # Создаем сессию, привязанную к этой транзакции
        async_session = async_sessionmaker(
            connection, expire_on_commit=False, class_=AsyncSession,
        )
        session = async_session()

        # Переопределяем зависимость get_db, чтобы возвращала эту сессию
        async def override_get_db():
            yield session

        app.dependency_overrides[get_db] = override_get_db

        yield session

        # Откатываем транзакцию после теста 
        await session.rollback()
        await connection.rollback()
        app.dependency_overrides.clear()


@pytest.fixture
def client(db_session) -> Generator[TestClient, None, None]:
    """Синхронный тестовый клиент FastAPI"""
    with TestClient(app=app) as test_client:
        yield test_client
