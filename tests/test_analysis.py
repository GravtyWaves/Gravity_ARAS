"""Tests for analysis API endpoints."""

import pytest
from httpx import AsyncClient


class TestAnalysisAPI:
    """Test cases for analysis API."""

    @pytest.mark.asyncio
    async def test_analyze_sentiment_success(self, client: AsyncClient):
        """Test successful sentiment analysis."""
        request_data = {"text": "This is a great article about positive news!", "language": "en"}

        response = await client.post("/api/v1/analysis/sentiment", json=request_data)

        assert response.status_code == 200
        data = response.json()

        assert data["success"] is True
        assert "analysis" in data["data"]
        analysis = data["data"]["analysis"]

        assert "sentiment" in analysis
        assert "confidence" in analysis
        assert isinstance(analysis["confidence"], (int, float))

    @pytest.mark.asyncio
    async def test_analyze_sentiment_persian(self, client: AsyncClient):
        """Test sentiment analysis for Persian text."""
        request_data = {"text": "این مقاله بسیار عالی و آموزنده است!", "language": "fa"}

        response = await client.post("/api/v1/analysis/sentiment", json=request_data)

        assert response.status_code == 200
        data = response.json()

        assert data["success"] is True
        assert "analysis" in data["data"]

    @pytest.mark.asyncio
    async def test_extract_entities_success(self, client: AsyncClient):
        """Test successful entity extraction."""
        request_data = {
            "text": "Barack Obama visited Microsoft headquarters in Seattle.",
            "language": "en",
        }

        response = await client.post("/api/v1/analysis/entities", json=request_data)

        assert response.status_code == 200
        data = response.json()

        assert data["success"] is True
        assert "entities" in data["data"]
        assert isinstance(data["data"]["entities"], list)

    @pytest.mark.asyncio
    async def test_extract_topics_success(self, client: AsyncClient):
        """Test successful topic extraction."""
        request_data = {
            "text": (
                "Machine learning and artificial intelligence are "
                "transforming technology industry."
            ),
            "language": "en",
            "num_topics": 3,
        }

        response = await client.post("/api/v1/analysis/topics", json=request_data)

        assert response.status_code == 200
        data = response.json()

        assert data["success"] is True
        assert "topics" in data["data"]
        assert isinstance(data["data"]["topics"], list)

    @pytest.mark.asyncio
    async def test_analyze_text_graph_success(self, client: AsyncClient):
        """Test successful text graph analysis."""
        request_data = {
            "text": (
                "John works at Google. Mary is John's colleague. "
                "They collaborate on AI projects."
            ),
            "language": "en",
        }

        response = await client.post("/api/v1/analysis/graph", json=request_data)

        assert response.status_code == 200
        data = response.json()

        assert data["success"] is True
        assert "graph" in data["data"]
        graph = data["data"]["graph"]

        assert "nodes" in graph
        assert "edges" in graph
        assert isinstance(graph["nodes"], list)
        assert isinstance(graph["edges"], list)

    @pytest.mark.asyncio
    async def test_batch_analysis_success(self, client: AsyncClient):
        """Test successful batch analysis."""
        request_data = {
            "texts": [
                "This is positive news.",
                "This is negative news.",
                "This is neutral information.",
            ],
            "language": "en",
            "analysis_types": ["sentiment", "entities"],
        }

        response = await client.post("/api/v1/analysis/batch", json=request_data)

        assert response.status_code == 200
        data = response.json()

        assert data["success"] is True
        assert "results" in data["data"]
        assert isinstance(data["data"]["results"], list)
        assert len(data["data"]["results"]) == 3

    @pytest.mark.asyncio
    async def test_analyze_sentiment_empty_text(self, client: AsyncClient):
        """Test sentiment analysis with empty text."""
        request_data = {"text": "", "language": "en"}

        response = await client.post("/api/v1/analysis/sentiment", json=request_data)

        assert response.status_code == 400
        data = response.json()

        assert data["success"] is False
        assert "Text cannot be empty" in data["message"]

    @pytest.mark.asyncio
    async def test_analyze_sentiment_invalid_language(self, client: AsyncClient):
        """Test sentiment analysis with invalid language."""
        request_data = {"text": "This is a test.", "language": "invalid"}

        response = await client.post("/api/v1/analysis/sentiment", json=request_data)

        assert response.status_code == 400
        data = response.json()

        assert data["success"] is False
        assert "Unsupported language" in data["message"]
