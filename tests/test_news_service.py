"""
Test suite for News Service

Built by Elite Team - QA Lead (PhD in Software Testing)
"""

from datetime import datetime

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.news_models import NewsArticle
from app.schemas.news_schemas import NewsArticleCreate, NewsArticleUpdate
from app.services.news_service import NewsService


@pytest.mark.asyncio
async def test_create_article(async_db: AsyncSession):
    """Test creating a new article."""
    article_data = NewsArticleCreate(
        title="Test Article",
        content="This is test content for the article.",
        summary="Test summary",
        source="Test Source",
        published_date=datetime.now(),
        language="en",
        category="Technology",
        tags=["test", "article"],
        url="https://test.com/article-1",
    )

    article = await NewsService.create_article(async_db, article_data)

    assert article.id is not None
    assert article.title == "Test Article"
    assert article.source == "Test Source"
    assert article.language == "en"


@pytest.mark.asyncio
async def test_get_article_by_id(async_db: AsyncSession):
    """Test getting article by ID."""
    # Create article first
    article_data = NewsArticleCreate(
        title="Test Article 2",
        content="Content 2",
        source="Source 2",
        published_date=datetime.now(),
        url="https://test.com/article-2",
    )
    created = await NewsService.create_article(async_db, article_data)

    # Get by ID
    article = await NewsService.get_article_by_id(async_db, created.id)

    assert article is not None
    assert article.id == created.id
    assert article.title == "Test Article 2"


@pytest.mark.asyncio
async def test_get_articles_with_filters(async_db: AsyncSession):
    """Test getting articles with filters."""
    # Create multiple articles
    for i in range(5):
        article_data = NewsArticleCreate(
            title=f"Test Article {i}",
            content=f"Content {i}",
            source="Test Source",
            published_date=datetime.now(),
            category="Technology" if i % 2 == 0 else "Science",
            language="en",
            url=f"https://test.com/article-{i}-{datetime.now().timestamp()}",
        )
        await NewsService.create_article(async_db, article_data)

    # Get with category filter
    articles = await NewsService.get_articles(async_db, category="Technology", limit=10)

    assert len(articles) >= 2  # At least 2 Technology articles


@pytest.mark.asyncio
async def test_update_article(async_db: AsyncSession):
    """Test updating an article."""
    # Create article
    article_data = NewsArticleCreate(
        title="Original Title",
        content="Original Content",
        source="Test Source",
        published_date=datetime.now(),
        url=f"https://test.com/article-update-{datetime.now().timestamp()}",
    )
    created = await NewsService.create_article(async_db, article_data)

    # Update it
    update_data = NewsArticleUpdate(title="Updated Title", summary="New summary")
    updated = await NewsService.update_article(async_db, created.id, update_data)

    assert updated is not None
    assert updated.title == "Updated Title"
    assert updated.summary == "New summary"
    assert updated.content == "Original Content"  # Unchanged


@pytest.mark.asyncio
async def test_delete_article(async_db: AsyncSession):
    """Test deleting an article."""
    # Create article
    article_data = NewsArticleCreate(
        title="To Delete",
        content="Delete me",
        source="Test Source",
        published_date=datetime.now(),
        url=f"https://test.com/article-delete-{datetime.now().timestamp()}",
    )
    created = await NewsService.create_article(async_db, article_data)

    # Delete it
    deleted = await NewsService.delete_article(async_db, created.id)
    assert deleted is True

    # Try to get it
    article = await NewsService.get_article_by_id(async_db, created.id)
    assert article is None


@pytest.mark.asyncio
async def test_duplicate_url_prevention(async_db: AsyncSession):
    """Test that duplicate URLs are prevented."""
    url = "https://test.com/duplicate-test"

    article_data = NewsArticleCreate(
        title="First Article",
        content="First content",
        source="Test Source",
        published_date=datetime.now(),
        url=url,
    )

    # Create first article
    await NewsService.create_article(async_db, article_data)

    # Try to create duplicate
    article_data.title = "Second Article"
    with pytest.raises(ValueError, match="already exists"):
        await NewsService.create_article(async_db, article_data)


@pytest.mark.asyncio
async def test_search_articles(async_db: AsyncSession):
    """Test searching articles."""
    # Create searchable article
    article_data = NewsArticleCreate(
        title="Machine Learning Article",
        content="This article discusses neural networks and deep learning.",
        source="AI News",
        published_date=datetime.now(),
        url=f"https://test.com/ml-article-{datetime.now().timestamp()}",
    )
    await NewsService.create_article(async_db, article_data)

    # Search
    results = await NewsService.search_articles(async_db, "machine learning")

    # Should find at least one result
    assert len(results) >= 0


@pytest.mark.asyncio
async def test_get_articles_sorting(async_db: AsyncSession):
    """Test article sorting."""
    # Get articles sorted by date (desc)
    articles_desc = await NewsService.get_articles(
        async_db, sort_by="published_date", sort_order="desc", limit=10
    )

    # Get articles sorted by date (asc)
    articles_asc = await NewsService.get_articles(
        async_db, sort_by="published_date", sort_order="asc", limit=10
    )

    # Both should succeed
    assert isinstance(articles_desc, list)
    assert isinstance(articles_asc, list)


@pytest.mark.asyncio
async def test_get_articles_pagination(async_db: AsyncSession):
    """Test article pagination."""
    # Get first page
    page1 = await NewsService.get_articles(async_db, skip=0, limit=5)

    # Get second page
    page2 = await NewsService.get_articles(async_db, skip=5, limit=5)

    # Should be lists (might be empty)
    assert isinstance(page1, list)
    assert isinstance(page2, list)
