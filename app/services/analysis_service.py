"""
ARAS Analysis Service
Wrapper for NLP operations

Built by Elite Team - Data Scientist (PhD in Data Science)
"""

from typing import Dict, List

from app.schemas.news_schemas import (
    EntitiesResponse,
    SentimentResponse,
    TopicsResponse,
)
from app.services.nlp_service import NLPService


class AnalysisService:
    """Service for NLP analysis operations."""

    @staticmethod
    async def analyze_sentiment(text: str, language: str = "en") -> SentimentResponse:
        """
        Analyze sentiment of text.
        
        Args:
            text: Input text
            language: Language code (en only for v1.0)
            
        Returns:
            SentimentResponse with sentiment classification and scores
        """
        if language != "en":
            raise ValueError("Only English ('en') is supported in v1.0")
        
        result = await NLPService.analyze_sentiment(text)
        
        return SentimentResponse(
            sentiment=result["sentiment"],
            score=result["polarity"],
            confidence=result["confidence"]
        )

    @staticmethod
    async def extract_entities(text: str, language: str = "en") -> EntitiesResponse:
        """
        Extract named entities from text.
        
        Args:
            text: Input text
            language: Language code (en only for v1.0)
            
        Returns:
            EntitiesResponse with extracted entities
        """
        if language != "en":
            raise ValueError("Only English ('en') is supported in v1.0")
        
        entities = await NLPService.extract_entities(text)
        
        return EntitiesResponse(entities=entities)

    @staticmethod
    async def extract_topics(text: str, language: str = "en") -> TopicsResponse:
        """
        Extract topics/keywords from text.
        
        Args:
            text: Input text
            language: Language code (en only for v1.0)
            
        Returns:
            TopicsResponse with extracted keywords
        """
        if language != "en":
            raise ValueError("Only English ('en') is supported in v1.0")
        
        keywords = await NLPService.extract_keywords(text, top_n=10)
        
        # Convert tuples to dict format
        topics = [{"keyword": word, "score": float(score)} for word, score in keywords]
        
        return TopicsResponse(topics=topics)
