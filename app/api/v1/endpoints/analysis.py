"""
Analysis API Endpoints
NLP and analytics operations

Built by Elite Team - Data Scientist (PhD in Data Science)
"""

from fastapi import APIRouter, HTTPException

from app.schemas.news_schemas import (
    AnalysisRequest,
    SentimentResponse,
    EntitiesResponse,
    TopicsResponse,
)
from app.services.analysis_service import AnalysisService

router = APIRouter()


@router.post("/sentiment", response_model=SentimentResponse)
async def analyze_sentiment(request: AnalysisRequest):
    """
    Analyze sentiment of text.
    
    Returns sentiment classification (positive/negative/neutral),
    polarity score (-1 to +1), and confidence (0 to 1).
    
    Example:
        POST /api/v1/analysis/sentiment
        {
            "text": "This is an excellent product!",
            "language": "en"
        }
    """
    try:
        result = await AnalysisService.analyze_sentiment(request.text, request.language)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Sentiment analysis failed: {str(e)}")


@router.post("/entities", response_model=EntitiesResponse)
async def extract_entities(request: AnalysisRequest):
    """
    Extract named entities from text.
    
    Recognizes: PERSON, ORG (organizations), GPE (geo-political entities),
    DATE, TIME, MONEY, PERCENT, CARDINAL, ORDINAL, and more.
    
    Example:
        POST /api/v1/analysis/entities
        {
            "text": "Apple Inc. CEO Tim Cook announced new iPhone in California.",
            "language": "en"
        }
    """
    try:
        result = await AnalysisService.extract_entities(request.text, request.language)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Entity extraction failed: {str(e)}")


@router.post("/topics", response_model=TopicsResponse)
async def extract_topics(request: AnalysisRequest):
    """
    Extract keywords/topics from text.
    
    Uses TF-IDF with POS filtering to identify most important
    keywords (nouns, proper nouns, adjectives).
    
    Example:
        POST /api/v1/analysis/topics
        {
            "text": "AI and machine learning are transforming healthcare.",
            "language": "en"
        }
    """
    try:
        result = await AnalysisService.extract_topics(request.text, request.language)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Topic extraction failed: {str(e)}")
