"""
Analysis API Endpoints
NLP and analytics operations

Built by Elite Team - Data Scientist (PhD in Data Science)
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.news_schemas import AnalysisRequest, APIResponse
from app.services.analysis_service import AnalysisService

router = APIRouter()


@router.post("/sentiment", response_model=APIResponse)
async def analyze_sentiment(request: AnalysisRequest, db: AsyncSession = Depends(get_db)):
    """Analyze sentiment of text."""
    try:
        result = await AnalysisService.analyze_sentiment(request.text, request.language)

        return APIResponse(
            success=True,
            message="Sentiment analysis completed",
            data={"sentiment": result.model_dump()},
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Sentiment analysis failed: {str(e)}")


@router.post("/entities", response_model=APIResponse)
async def extract_entities(request: AnalysisRequest, db: AsyncSession = Depends(get_db)):
    """Extract named entities from text."""
    try:
        result = await AnalysisService.extract_entities(request.text, request.language)

        return APIResponse(
            success=True,
            message="Entity extraction completed",
            data={"entities": result.model_dump()},
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Entity extraction failed: {str(e)}")


@router.post("/topics", response_model=APIResponse)
async def extract_topics(request: AnalysisRequest, db: AsyncSession = Depends(get_db)):
    """Extract topics from text using topic modeling."""
    try:
        result = await AnalysisService.extract_topics(request.text, request.language)

        return APIResponse(
            success=True, message="Topic modeling completed", data={"topics": result.model_dump()}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Topic modeling failed: {str(e)}")


@router.post("/graph", response_model=APIResponse)
async def analyze_graph(request: AnalysisRequest, db: AsyncSession = Depends(get_db)):
    """Perform graph analysis on text relationships."""
    try:
        result = await AnalysisService.analyze_graph(request.text, request.language)

        return APIResponse(
            success=True, message="Graph analysis completed", data={"graph": result.model_dump()}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Graph analysis failed: {str(e)}")


@router.post("/comprehensive", response_model=APIResponse)
async def comprehensive_analysis(request: AnalysisRequest, db: AsyncSession = Depends(get_db)):
    """Perform comprehensive analysis (sentiment, entities, topics, graph)."""
    try:
        sentiment = await AnalysisService.analyze_sentiment(request.text, request.language)
        entities = await AnalysisService.extract_entities(request.text, request.language)
        topics = await AnalysisService.extract_topics(request.text, request.language)
        graph = await AnalysisService.analyze_graph(request.text, request.language)

        return APIResponse(
            success=True,
            message="Comprehensive analysis completed",
            data={
                "sentiment": sentiment.model_dump(),
                "entities": entities.model_dump(),
                "topics": topics.model_dump(),
                "graph": graph.model_dump(),
            },
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Comprehensive analysis failed: {str(e)}")


@router.post("/batch-sentiment", response_model=APIResponse)
async def batch_sentiment_analysis(
    texts: list[AnalysisRequest], db: AsyncSession = Depends(get_db)
):
    """Analyze sentiment for multiple texts."""
    try:
        results = []
        for req in texts:
            result = await AnalysisService.analyze_sentiment(req.text, req.language)
            results.append(result.model_dump())

        return APIResponse(
            success=True,
            message=f"Batch sentiment analysis completed for {len(results)} texts",
            data={"results": results},
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Batch sentiment analysis failed: {str(e)}")
