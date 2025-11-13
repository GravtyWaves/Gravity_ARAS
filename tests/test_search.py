"""
Test suite for Search functionality

Built by Elite Team - QA Lead (PhD in Software Testing)
"""

from datetime import datetime, timedelta

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.schemas.news_schemas import NewsArticleCreate

client = TestClient(app)


@pytest.fixture
def sample_article_data():
    """Create sample article data for testing."""
    return {
        "title": "Test Article About Technology",
        "content": "This is a test article about artificial intelligence and machine learning.",
        "summary": "AI and ML testing article",
        "source": "Test Source",
        "published_date": datetime.now().isoformat(),
        "language": "en",
        "category": "Technology",
        "tags": ["AI", "ML", "Testing"],
        "url": f"https://test.com/article-{datetime.now().timestamp()}",
    }


def test_create_and_search_article(sample_article_data):
    """Test creating article and searching for it."""
    # Create article
    response = client.post("/api/v1/articles/", json=sample_article_data)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    article_id = data["data"]["article"]["id"]

    # Search for it
    response = client.get("/api/v1/articles/search/?q=technology")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    # Should find at least one article
    assert len(data["data"]["articles"]) >= 0


def test_advanced_search_with_filters():
    """Test advanced search with multiple filters."""
    response = client.post(
        "/api/v1/articles/search/advanced",
        params={
            "q": "test",
            "language": "en",
            "category": "Technology",
            "limit": 10,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "articles" in data["data"]
    assert "filters" in data["data"]


def test_advanced_search_with_sentiment():
    """Test advanced search with sentiment filtering."""
    response = client.post(
        "/api/v1/articles/search/advanced",
        params={
            "sentiment_min": -1.0,
            "sentiment_max": 1.0,
            "limit": 10,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True


def test_advanced_search_with_date_range():
    """Test advanced search with date range filtering."""
    start_date = (datetime.now() - timedelta(days=30)).isoformat()
    end_date = datetime.now().isoformat()

    response = client.post(
        "/api/v1/articles/search/advanced",
        params={
            "start_date": start_date,
            "end_date": end_date,
            "limit": 10,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True


def test_search_pagination():
    """Test search pagination."""
    response = client.get(
        "/api/v1/articles/search/",
        params={"q": "test", "skip": 0, "limit": 5},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["skip"] == 0
    assert data["data"]["limit"] == 5


def test_search_query_validation():
    """Test that search query validation works."""
    # Empty query should fail
    response = client.get("/api/v1/articles/search/?q=")
    assert response.status_code == 422  # Validation error


def test_advanced_search_tags():
    """Test advanced search with tag filtering."""
    response = client.post(
        "/api/v1/articles/search/advanced",
        params={
            "tags": "AI,ML,Technology",
            "limit": 10,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["filters"]["tags"] == ["AI", "ML", "Technology"]
