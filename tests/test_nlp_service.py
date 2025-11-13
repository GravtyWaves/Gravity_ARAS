"""
Comprehensive NLP Service Tests
95%+ coverage target for v1.0.0

Built by Elite Team - Testing Specialist
"""

import pytest
from unittest.mock import Mock, patch

from app.nlp.spacy_engine import SpacyNLPEngine, get_nlp_engine


class TestSpacyNLPEngine:
    """Test suite for SpacyNLPEngine."""

    @pytest.fixture
    def engine(self):
        """Get NLP engine instance."""
        return get_nlp_engine()

    def test_singleton_pattern(self):
        """Test that get_nlp_engine returns same instance."""
        engine1 = get_nlp_engine()
        engine2 = get_nlp_engine()
        assert engine1 is engine2

    def test_model_loaded(self, engine):
        """Test that spaCy model is loaded."""
        assert engine.is_loaded()
        assert engine.nlp is not None

    @pytest.mark.asyncio
    async def test_sentiment_positive(self, engine):
        """Test positive sentiment detection."""
        text = "This is excellent news! The economy is improving and growth is strong."
        result = await engine.analyze_sentiment_async(text)
        
        assert result["sentiment"] == "positive"
        assert result["polarity"] > 0
        assert result["confidence"] > 0.5

    @pytest.mark.asyncio
    async def test_sentiment_negative(self, engine):
        """Test negative sentiment detection."""
        text = "This is terrible news. The crisis is worsening and the situation is bad."
        result = await engine.analyze_sentiment_async(text)
        
        assert result["sentiment"] == "negative"
        assert result["polarity"] < 0
        assert result["confidence"] > 0.5

    @pytest.mark.asyncio
    async def test_sentiment_neutral(self, engine):
        """Test neutral sentiment detection."""
        text = "The meeting is scheduled for Monday at 3pm in the conference room."
        result = await engine.analyze_sentiment_async(text)
        
        assert result["sentiment"] == "neutral"
        assert result["polarity"] >= -0.3
        assert result["polarity"] <= 0.3

    @pytest.mark.asyncio
    async def test_sentiment_empty_text(self, engine):
        """Test sentiment with empty text."""
        result = await engine.analyze_sentiment_async("")
        
        assert result["sentiment"] == "neutral"
        assert result["polarity"] == 0.0
        assert result["confidence"] == 0.5

    def test_sentiment_sync(self, engine):
        """Test synchronous sentiment analysis."""
        text = "Great performance and outstanding results!"
        result = engine.analyze_sentiment(text)
        
        assert result["sentiment"] == "positive"
        assert "polarity" in result
        assert "confidence" in result

    @pytest.mark.asyncio
    async def test_entity_extraction_person(self, engine):
        """Test PERSON entity extraction."""
        text = "Tim Cook announced the new iPhone yesterday."
        entities = await engine.extract_entities_async(text)
        
        person_entities = [e for e in entities if e["label"] == "PERSON"]
        assert len(person_entities) > 0
        assert any("Tim Cook" in e["text"] or "Cook" in e["text"] for e in person_entities)

    @pytest.mark.asyncio
    async def test_entity_extraction_org(self, engine):
        """Test ORG entity extraction."""
        text = "Apple Inc. and Microsoft Corporation announced a new partnership."
        entities = await engine.extract_entities_async(text)
        
        org_entities = [e for e in entities if e["label"] == "ORG"]
        assert len(org_entities) >= 1

    @pytest.mark.asyncio
    async def test_entity_extraction_gpe(self, engine):
        """Test GPE (location) entity extraction."""
        text = "The conference will be held in San Francisco, California."
        entities = await engine.extract_entities_async(text)
        
        gpe_entities = [e for e in entities if e["label"] == "GPE"]
        assert len(gpe_entities) >= 1

    @pytest.mark.asyncio
    async def test_entity_extraction_date(self, engine):
        """Test DATE entity extraction."""
        text = "The meeting is scheduled for January 15, 2025."
        entities = await engine.extract_entities_async(text)
        
        date_entities = [e for e in entities if e["label"] == "DATE"]
        assert len(date_entities) >= 1

    @pytest.mark.asyncio
    async def test_entity_extraction_empty(self, engine):
        """Test entity extraction with no entities."""
        text = "nothing special here"
        entities = await engine.extract_entities_async(text)
        
        assert isinstance(entities, list)
        # May be empty or have minimal entities

    def test_entity_extraction_sync(self, engine):
        """Test synchronous entity extraction."""
        text = "Barack Obama was the president of the United States."
        entities = engine.extract_entities(text)
        
        assert isinstance(entities, list)
        assert len(entities) > 0
        assert all("text" in e and "label" in e for e in entities)

    @pytest.mark.asyncio
    async def test_keyword_extraction(self, engine):
        """Test keyword extraction."""
        text = """
        Artificial intelligence and machine learning are transforming healthcare.
        Medical professionals are using AI to diagnose diseases more accurately.
        Machine learning algorithms analyze patient data to predict outcomes.
        """
        keywords = await engine.extract_keywords_async(text, top_n=5)
        
        assert isinstance(keywords, list)
        assert len(keywords) > 0
        assert len(keywords) <= 5
        
        # Keywords are tuples of (word, score)
        for kw, score in keywords:
            assert isinstance(kw, str)
            assert isinstance(score, float)

    @pytest.mark.asyncio
    async def test_keyword_extraction_max_keywords(self, engine):
        """Test keyword extraction with top_n parameter."""
        text = "technology innovation software development programming python java javascript"
        keywords = await engine.extract_keywords_async(text, top_n=3)
        
        assert len(keywords) <= 3

    def test_keyword_extraction_sync(self, engine):
        """Test synchronous keyword extraction."""
        text = "Climate change and global warming are environmental concerns."
        keywords = engine.extract_keywords(text, top_n=10)
        
        assert isinstance(keywords, list)
        assert all(isinstance(kw, tuple) and len(kw) == 2 for kw in keywords)

    @pytest.mark.asyncio
    async def test_summarization(self, engine):
        """Test text summarization."""
        text = """
        The new policy will take effect next month. Officials announced the changes yesterday.
        The policy aims to improve efficiency. Many stakeholders have expressed support.
        Implementation will begin in January. Training sessions are scheduled for staff.
        """
        summary = await engine.summarize_async(text, ratio=0.5)
        
        assert isinstance(summary, str)
        assert len(summary) > 0
        assert len(summary) < len(text)

    @pytest.mark.asyncio
    async def test_summarization_short_text(self, engine):
        """Test summarization with short text."""
        text = "This is a short sentence."
        summary = await engine.summarize_async(text)
        
        # Should return original for very short text
        assert summary == text

    @pytest.mark.asyncio
    async def test_topic_analysis_single_doc(self, engine):
        """Test topic analysis with multiple documents."""
        texts = [
            "AI and machine learning are transforming technology",
            "Healthcare professionals use AI for diagnostics",
            "Machine learning algorithms improve accuracy",
            "Medical technology advances with AI",
            "Software development uses AI tools"
        ]
        topics = await engine.analyze_topics_async(texts, num_topics=2)
        
        assert isinstance(topics, list)
        assert len(topics) > 0
        
        # Each topic should be a list of words
        for topic in topics:
            assert isinstance(topic, list)
            assert all(isinstance(word, str) for word in topic)

    def test_model_not_loaded_error(self):
        """Test error when model not loaded."""
        engine = SpacyNLPEngine.__new__(SpacyNLPEngine)
        engine._model_loaded = False
        engine.nlp = None
        
        with pytest.raises(RuntimeError, match="Model not loaded"):
            engine.analyze_sentiment("test")

    @pytest.mark.asyncio
    async def test_concurrent_sentiment_analysis(self, engine):
        """Test concurrent sentiment analysis."""
        import asyncio
        
        texts = [
            "Great product!",
            "Terrible service.",
            "It's okay.",
            "Excellent quality!",
            "Very disappointing."
        ]
        
        tasks = [engine.analyze_sentiment_async(text) for text in texts]
        results = await asyncio.gather(*tasks)
        
        assert len(results) == 5
        assert all("sentiment" in r for r in results)

    @pytest.mark.asyncio
    async def test_concurrent_entity_extraction(self, engine):
        """Test concurrent entity extraction."""
        import asyncio
        
        texts = [
            "Tim Cook leads Apple",
            "Microsoft is based in Redmond",
            "Google CEO Sundar Pichai"
        ]
        
        tasks = [engine.extract_entities_async(text) for text in texts]
        results = await asyncio.gather(*tasks)
        
        assert len(results) == 3
        assert all(isinstance(r, list) for r in results)

    def test_sentiment_with_mixed_signals(self, engine):
        """Test sentiment with both positive and negative words."""
        text = "The product is great but the price is terrible"
        result = engine.analyze_sentiment(text)
        
        # Should detect mixed sentiment
        assert "sentiment" in result
        assert result["confidence"] >= 0.0

    def test_entity_positions(self, engine):
        """Test that entity positions are correct."""
        text = "Apple announced new iPhone"
        entities = engine.extract_entities(text)
        
        for entity in entities:
            assert "start" in entity
            assert "end" in entity
            assert entity["start"] < entity["end"]
            assert text[entity["start"]:entity["end"]] == entity["text"]

    @pytest.mark.asyncio
    async def test_keyword_extraction_filtering(self, engine):
        """Test that keywords are properly filtered (no stop words)."""
        text = "the and or but is are was were"
        keywords = await engine.extract_keywords_async(text, top_n=10)
        
        # Should not extract stop words
        assert len(keywords) == 0

    @pytest.mark.asyncio
    async def test_error_handling_sentiment(self, engine):
        """Test error handling in sentiment analysis."""
        # Very long text that might cause issues
        text = "word " * 10000
        result = await engine.analyze_sentiment_async(text)
        
        # Should still return valid result
        assert "sentiment" in result
        assert "polarity" in result

    def test_load_model_twice(self, engine):
        """Test that loading model twice doesn't cause issues."""
        result1 = engine.load_model()
        result2 = engine.load_model()
        
        assert result1 is True
        assert result2 is True
        assert engine.is_loaded()
