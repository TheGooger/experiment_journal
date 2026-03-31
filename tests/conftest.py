import pytest
import asyncio
import os
import uuid
from dotenv import load_dotenv
from typing import AsyncGenerator
from httpx import AsyncClient, ASGITransport

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.pool import NullPool

from app.db.models.base import Base
from app.db.models.user import User
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
async def async_client(db_session) -> AsyncGenerator[AsyncClient, None]:
    """Синхронный тестовый клиент FastAPI"""
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as test_client:
        yield test_client


@pytest.fixture
async def test_user(db_session):
    user = User(
        id=uuid.uuid4(),
        user_name=f"vova_test_{uuid.uuid4()}",
        hashed_password="fake",
    )

    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    return user 


@pytest.fixture
async def auth_headers(async_client: AsyncClient):
    username = f"user_{uuid.uuid4()}"

    await async_client.post(
        "/auth/register",
        json={
            "user_name": username,
            "password": "123456"
        }
    )

    response = await async_client.post(
        "/auth/login",
        data={
            "username": username,
            "password": "123456"
        }
    )

    token = response.json()["access_token"]

    return {"Authorization": f"Bearer {token}"}