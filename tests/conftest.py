"""Pytest configuration and fixtures for ARAS microservice tests."""

import asyncio
from typing import AsyncGenerator, Generator

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.database import get_db
from app.main import app
from app.models.news_models import Base

# Test database URL
TEST_DATABASE_URL = "sqlite+aiosqlite:///./test.db"


@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def test_engine():
    """Create test database engine."""
    engine = create_async_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        echo=False,
    )

    # Create all tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    # Drop all tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def test_db_session(test_engine) -> AsyncGenerator[AsyncSession, None]:
    """Create test database session."""
    async_session = sessionmaker(test_engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as session:
        yield session


@pytest.fixture
async def client(test_db_session) -> AsyncGenerator[AsyncClient, None]:
    """Create test client with database session override."""

    async def override_get_db():
        yield test_db_session

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(app=app, base_url="http://testserver") as client:
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
async def sample_article_data():
    """Sample article data for testing."""
    return {
        "title": "Test Article",
        "content": "This is a test article content for testing purposes.",
        "url": "https://example.com/test-article",
        "source": "Test Source",
        "published_date": "2024-01-01T00:00:00Z",
        "language": "en",
        "tags": ["test", "article"],
    }


@pytest.fixture
async def sample_entity_data():
    """Sample entity data for testing."""
    return {
        "name": "Test Entity",
        "type": "PERSON",
        "confidence": 0.95,
        "mentions": 5,
        "first_mention": "2024-01-01T00:00:00Z",
        "last_mention": "2024-01-01T12:00:00Z",
    }


@pytest.fixture
async def sample_trend_data():
    """Sample trend data for testing."""
    return {
        "topic": "Test Trend",
        "keywords": ["test", "trend", "analysis"],
        "frequency": 100,
        "sentiment_score": 0.7,
        "start_date": "2024-01-01T00:00:00Z",
        "end_date": "2024-01-02T00:00:00Z",
        "is_active": True,
    }
