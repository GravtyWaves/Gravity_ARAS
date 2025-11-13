"""Tests for articles API endpoints."""

import pytest
from httpx import AsyncClient


class TestArticlesAPI:
    """Test cases for articles API."""

    @pytest.mark.asyncio
    async def test_create_article_success(self, client: AsyncClient, sample_article_data):
        """Test successful article creation."""
        response = await client.post("/api/v1/articles/", json=sample_article_data)

        assert response.status_code == 201
        data = response.json()

        assert data["success"] is True
        assert "article" in data["data"]
        article = data["data"]["article"]

        assert article["title"] == sample_article_data["title"]
        assert article["content"] == sample_article_data["content"]
        assert article["url"] == sample_article_data["url"]
        assert article["source"] == sample_article_data["source"]
        assert article["language"] == sample_article_data["language"]
        assert article["tags"] == sample_article_data["tags"]

    @pytest.mark.asyncio
    async def test_get_articles_list(self, client: AsyncClient, sample_article_data):
        """Test getting list of articles."""
        # Create an article first
        create_response = await client.post("/api/v1/articles/", json=sample_article_data)
        assert create_response.status_code == 201

        # Get articles list
        response = await client.get("/api/v1/articles/")

        assert response.status_code == 200
        data = response.json()

        assert data["success"] is True
        assert "articles" in data["data"]
        assert len(data["data"]["articles"]) >= 1

    @pytest.mark.asyncio
    async def test_get_article_by_id(self, client: AsyncClient, sample_article_data):
        """Test getting specific article by ID."""
        # Create an article first
        create_response = await client.post("/api/v1/articles/", json=sample_article_data)
        assert create_response.status_code == 201
        created_article = create_response.json()["data"]["article"]

        # Get the article by ID
        response = await client.get(f"/api/v1/articles/{created_article['id']}")

        assert response.status_code == 200
        data = response.json()

        assert data["success"] is True
        assert "article" in data["data"]
        article = data["data"]["article"]

        assert article["id"] == created_article["id"]
        assert article["title"] == sample_article_data["title"]

    @pytest.mark.asyncio
    async def test_update_article(self, client: AsyncClient, sample_article_data):
        """Test updating an article."""
        # Create an article first
        create_response = await client.post("/api/v1/articles/", json=sample_article_data)
        assert create_response.status_code == 201
        created_article = create_response.json()["data"]["article"]

        # Update the article
        update_data = sample_article_data.copy()
        update_data["title"] = "Updated Test Article"

        response = await client.put(f"/api/v1/articles/{created_article['id']}", json=update_data)

        assert response.status_code == 200
        data = response.json()

        assert data["success"] is True
        assert "article" in data["data"]
        article = data["data"]["article"]

        assert article["title"] == "Updated Test Article"
        assert article["id"] == created_article["id"]

    @pytest.mark.asyncio
    async def test_delete_article(self, client: AsyncClient, sample_article_data):
        """Test deleting an article."""
        # Create an article first
        create_response = await client.post("/api/v1/articles/", json=sample_article_data)
        assert create_response.status_code == 201
        created_article = create_response.json()["data"]["article"]

        # Delete the article
        response = await client.delete(f"/api/v1/articles/{created_article['id']}")

        assert response.status_code == 200
        data = response.json()

        assert data["success"] is True

        # Verify article is deleted
        get_response = await client.get(f"/api/v1/articles/{created_article['id']}")
        assert get_response.status_code == 404

    @pytest.mark.asyncio
    async def test_search_articles(self, client: AsyncClient, sample_article_data):
        """Test searching articles."""
        # Create an article first
        create_response = await client.post("/api/v1/articles/", json=sample_article_data)
        assert create_response.status_code == 201

        # Search for articles
        response = await client.get("/api/v1/articles/search/?query=test")

        assert response.status_code == 200
        data = response.json()

        assert data["success"] is True
        assert "articles" in data["data"]
        assert len(data["data"]["articles"]) >= 1

    @pytest.mark.asyncio
    async def test_get_article_not_found(self, client: AsyncClient):
        """Test getting non-existent article."""
        response = await client.get("/api/v1/articles/99999")

        assert response.status_code == 404
        data = response.json()

        assert data["success"] is False
        assert "Article not found" in data["message"]
