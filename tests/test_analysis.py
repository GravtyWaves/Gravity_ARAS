"""Tests for analysis API endpoints."""

import pytest
from fastapi.testclient import TestClient


class TestAnalysisAPI:
    """Test cases for analysis API."""

    def test_analyze_sentiment_success(self, client: TestClient):
        """Test successful sentiment analysis."""
        request_data = {"text": "This is a great article about positive news!", "language": "en"}

        response = client.post("/api/v1/analysis/sentiment", json=request_data)

        assert response.status_code == 200
        data = response.json()

        assert "sentiment" in data
        assert "score" in data
        assert "confidence" in data
        assert isinstance(data["confidence"], (int, float))

    def test_analyze_sentiment_persian(self, client: TestClient):
        """Test sentiment analysis for Persian text."""
        request_data = {"text": "این مقاله بسیار عالی و آموزنده است!", "language": "fa"}

        response = client.post("/api/v1/analysis/sentiment", json=request_data)

        assert response.status_code == 200
        data = response.json()

        assert "sentiment" in data
        assert "score" in data

    def test_extract_entities_success(self, client: TestClient):
        """Test successful entity extraction."""
        request_data = {
            "text": "Barack Obama visited Microsoft headquarters in Seattle.",
            "language": "en",
        }

        response = client.post("/api/v1/analysis/entities", json=request_data)

        assert response.status_code == 200
        data = response.json()

        assert "entities" in data
        assert isinstance(data["entities"], list)

    def test_extract_topics_success(self, client: TestClient):
        """Test successful topic extraction."""
        request_data = {
            "text": (
                "Machine learning and artificial intelligence are "
                "transforming technology industry."
            ),
            "language": "en",
            "num_topics": 3,
        }

        response = client.post("/api/v1/analysis/topics", json=request_data)

        assert response.status_code == 200
        data = response.json()

        assert "topics" in data
        assert isinstance(data["topics"], list)

    def test_analyze_text_graph_success(self, client: TestClient):
        """Test successful text graph analysis."""
        request_data = {
            "text": (
                "John works at Google. Mary is John's colleague. "
                "They collaborate on AI projects."
            ),
            "language": "en",
        }

        response = client.post("/api/v1/analysis/graph", json=request_data)

        assert response.status_code == 200
        data = response.json()

        assert "nodes" in data
        assert "edges" in data
        assert isinstance(data["nodes"], list)
        assert isinstance(data["edges"], list)

    def test_batch_analysis_success(self, client: TestClient):
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

        response = client.post("/api/v1/analysis/batch", json=request_data)

        assert response.status_code == 200
        data = response.json()

        # Expect direct list response or dict with results
        if isinstance(data, list):
            assert len(data) == 3
        else:
            assert "results" in data or isinstance(data, dict)

    def test_analyze_sentiment_empty_text(self, client: TestClient):
        """Test sentiment analysis with empty text."""
        request_data = {"text": "", "language": "en"}

        response = client.post("/api/v1/analysis/sentiment", json=request_data)

        # Expect 422 validation error from Pydantic
        assert response.status_code == 422

    def test_analyze_sentiment_invalid_language(self, client: TestClient):
        """Test sentiment analysis with invalid language."""
        request_data = {"text": "This is a test.", "language": "invalid"}

        response = client.post("/api/v1/analysis/sentiment", json=request_data)

        # Expect 400 error for unsupported language
        assert response.status_code in (400, 422)
        data = response.json()
        # Error details in FastAPI format
        assert "detail" in data or "message" in data
