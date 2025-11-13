"""
ARAS NLP Service - Production Implementation
Uses spaCy engine for English news analysis

Built by Elite Team - Data Scientist (PhD in NLP)
"""

import logging
from typing import Dict, List

from app.nlp.spacy_engine import get_nlp_engine

logger = logging.getLogger(__name__)


class NLPService:
    """Production NLP service using spaCy engine."""

    @staticmethod
    async def analyze_sentiment(text: str) -> Dict:
        """Analyze sentiment of text."""
        engine = get_nlp_engine()
        return await engine.analyze_sentiment_async(text)

    @staticmethod
    async def extract_entities(text: str) -> List[Dict]:
        """Extract named entities from text."""
        engine = get_nlp_engine()
        return await engine.extract_entities_async(text)

    @staticmethod
    async def extract_keywords(text: str, top_n: int = 10) -> List[tuple]:
        """Extract top keywords from text."""
        engine = get_nlp_engine()
        return await engine.extract_keywords_async(text, top_n)

    @staticmethod
    async def summarize_text(text: str, ratio: float = 0.3) -> str:
        """Generate extractive summary of text."""
        engine = get_nlp_engine()
        return await engine.summarize_async(text, ratio)

    @staticmethod
    async def analyze_topics(texts: List[str], num_topics: int = 5) -> List[List[str]]:
        """Perform topic modeling on multiple texts."""
        engine = get_nlp_engine()
        return await engine.analyze_topics_async(texts, num_topics)
