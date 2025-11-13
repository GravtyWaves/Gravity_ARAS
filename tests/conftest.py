"""Pytest configuration and fixtures for ARAS microservice tests."""

import asyncio
from typing import AsyncGenerator, Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.database import get_db
from app.main import app
from app.models.news_models import Base

# Test database URLs
ASYNC_TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"
SYNC_TEST_DATABASE_URL = "sqlite:///:memory:"


@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
def sync_db_session() -> Generator[Session, None, None]:
    """Create synchronous database session for API tests."""
    engine = create_engine(
        SYNC_TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()
    
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="session")
async def test_engine():
    """Create test database engine for async tests."""
    engine = create_async_engine(
        ASYNC_TEST_DATABASE_URL,
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
async def async_db(test_db_session) -> AsyncSession:
    """Provide async database session for service tests."""
    return test_db_session


@pytest.fixture
async def test_db_session(test_engine) -> AsyncGenerator[AsyncSession, None]:
    """Create test database session for async tests."""
    async_session = sessionmaker(test_engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as session:
        async with session.begin():
            yield session
            await session.rollback()


@pytest.fixture
def client(sync_db_session) -> Generator[TestClient, None, None]:
    """Create test client with database session override."""

    def override_get_db():
        try:
            yield sync_db_session
        finally:
            sync_db_session.rollback()

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as tc:
        yield tc

    app.dependency_overrides.clear()


@pytest.fixture
async def sample_article_data():
    """Sample article data for testing."""
    return {
        "title": "Test Article",
        "content": "This is a test article content for testing purposes.",
        "url": "https://example.com/test-article",
        "source": "Test Source",
        "published_date": "2024-01-01T00:00:00",
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
        "first_mention": "2024-01-01T00:00:00",
        "last_mention": "2024-01-01T12:00:00",
    }


@pytest.fixture
async def sample_trend_data():
    """Sample trend data for testing."""
    return {
        "topic": "Test Trend",
        "keywords": ["test", "trend", "analysis"],
        "frequency": 100,
        "sentiment_score": 0.7,
        "start_date": "2024-01-01T00:00:00",
        "end_date": "2024-01-02T00:00:00",
        "is_active": True,
    }
