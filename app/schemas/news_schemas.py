"""
ARAS Microservice Pydantic Schemas
Request/Response validation models

Built by Elite Team - Backend Developers (PhD in Software Engineering)
"""

from datetime import datetime
from typing import Dict, List, Optional

from pydantic import BaseModel, Field, HttpUrl


class NewsArticleBase(BaseModel):
    """Base schema for news articles."""

    title: str = Field(..., min_length=1, max_length=500)
    content: str = Field(..., min_length=1)
    summary: Optional[str] = None
    source: str = Field(..., min_length=1, max_length=255)
    published_date: datetime
    language: str = Field(default="en", min_length=2, max_length=10)
    category: Optional[str] = Field(None, max_length=100)
    tags: List[str] = Field(default_factory=list)
    sentiment_score: float = Field(default=0.0, ge=-1.0, le=1.0)
    entities: List[Dict] = Field(default_factory=list)
    topics: List[Dict] = Field(default_factory=list)
    url: HttpUrl


class NewsArticleCreate(NewsArticleBase):
    """Schema for creating news articles."""
    pass


class NewsArticleUpdate(BaseModel):
    """Schema for updating news articles."""

    title: Optional[str] = Field(None, min_length=1, max_length=500)
    content: Optional[str] = Field(None, min_length=1)
    summary: Optional[str] = None
    category: Optional[str] = Field(None, max_length=100)
    tags: Optional[List[str]] = None
    sentiment_score: Optional[float] = Field(None, ge=-1.0, le=1.0)
    entities: Optional[List[Dict]] = None
    topics: Optional[List[Dict]] = None


class NewsArticle(NewsArticleBase):
    """Schema for news article responses."""

    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class EntityBase(BaseModel):
    """Base schema for entities."""

    name: str = Field(..., min_length=1, max_length=255)
    type: str = Field(..., min_length=1, max_length=50)
    aliases: List[str] = Field(default_factory=list)
    attributes: Dict = Field(default_factory=dict)
    confidence_score: float = Field(default=1.0, ge=0.0, le=1.0)


class EntityCreate(EntityBase):
    """Schema for creating entities."""
    pass


class EntityUpdate(BaseModel):
    """Schema for updating entities."""

    name: Optional[str] = Field(None, min_length=1, max_length=255)
    type: Optional[str] = Field(None, min_length=1, max_length=50)
    aliases: Optional[List[str]] = None
    attributes: Optional[Dict] = None
    confidence_score: Optional[float] = Field(None, ge=0.0, le=1.0)


class Entity(EntityBase):
    """Schema for entity responses."""

    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class TrendBase(BaseModel):
    """Base schema for trends."""

    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    start_date: datetime
    peak_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    confidence_score: float = Field(default=0.0, ge=0.0, le=1.0)
    impact_level: str = Field(default="low")
    keywords: List[str] = Field(default_factory=list)


class TrendCreate(TrendBase):
    """Schema for creating trends."""
    pass


class TrendUpdate(BaseModel):
    """Schema for updating trends."""

    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    peak_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    confidence_score: Optional[float] = Field(None, ge=0.0, le=1.0)
    impact_level: Optional[str] = None
    keywords: Optional[List[str]] = None


class Trend(TrendBase):
    """Schema for trend responses."""

    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class AnalysisRequest(BaseModel):
    """Schema for analysis requests."""

    text: str = Field(..., min_length=1)
    language: str = Field(default="en", min_length=2, max_length=10)


class SentimentResponse(BaseModel):
    """Schema for sentiment analysis responses."""

    sentiment: str  # positive, negative, neutral
    score: float = Field(ge=-1.0, le=1.0)
    confidence: float = Field(ge=0.0, le=1.0)


class EntitiesResponse(BaseModel):
    """Schema for entity extraction responses."""

    entities: List[Dict]  # List of extracted entities with positions


class TopicsResponse(BaseModel):
    """Schema for topic modeling responses."""

    topics: List[Dict]  # List of topics with keywords and weights


class GraphAnalysisResponse(BaseModel):
    """Schema for graph analysis responses."""

    nodes: List[Dict]
    edges: List[Dict]
    metrics: Dict  # centrality, clustering, etc.


class APIResponse(BaseModel):
    """Generic API response schema."""

    success: bool
    message: str
    data: Optional[Dict] = None
    errors: Optional[List[str]] = None