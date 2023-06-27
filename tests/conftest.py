import os
from typing import AsyncGenerator, Generator, Callable

import asyncio
import pytest_asyncio
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

from api.models import Base


load_dotenv()

SQLALCHEMY_TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")

engine = create_async_engine(SQLALCHEMY_TEST_DATABASE_URL)
test_async_session = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


@pytest_asyncio.fixture(scope="session")
def event_loop(request) -> Generator:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture()
async def get_session() -> AsyncSession:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        async with test_async_session(bind=conn) as session:
            yield session
            await session.flush()
            await session.rollback()


@pytest_asyncio.fixture()
def override_get_db(get_session: AsyncSession) -> Callable:
    async def _override_get_db():
        yield get_session

    return _override_get_db


@pytest_asyncio.fixture()
def app(override_get_db: Callable) -> FastAPI:
    from api.database import get_session
    from main import app

    app.dependency_overrides[get_session] = override_get_db
    return app


@pytest_asyncio.fixture()
async def async_client(app: FastAPI) -> AsyncGenerator:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
