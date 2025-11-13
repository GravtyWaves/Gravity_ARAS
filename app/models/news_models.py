"""
ARAS Microservice Data Models
SQLAlchemy models for news analysis

Built by Elite Team - Database Engineer (PhD in Database Systems)
"""

from datetime import datetime
from typing import Dict, List, Optional

from sqlalchemy import Column, DateTime, Float, Integer, String, Text, JSON
from sqlalchemy.sql import func

from app.core.database import Base


class NewsArticle(Base):
    """News article model."""

    __tablename__ = "news_articles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), nullable=False, index=True)
    content = Column(Text, nullable=False)
    summary = Column(Text)
    source = Column(String(255), nullable=False, index=True)
    published_date = Column(DateTime, nullable=False, index=True)
    language = Column(String(10), default="en")
    category = Column(String(100), index=True)
    tags = Column(JSON, default=list)  # List of tags
    sentiment_score = Column(Float, default=0.0)  # -1 to 1
    entities = Column(JSON, default=list)  # Extracted entities
    topics = Column(JSON, default=list)  # Topic modeling results
    url = Column(String(1000), unique=True, index=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<NewsArticle(id={self.id}, title='{self.title[:50]}...')>"


class Entity(Base):
    """Named entity model."""

    __tablename__ = "entities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    type = Column(String(50), nullable=False, index=True)  # PERSON, ORG, LOCATION, etc.
    aliases = Column(JSON, default=list)  # Alternative names
    attributes = Column(JSON, default=dict)  # Additional attributes
    confidence_score = Column(Float, default=1.0)
    created_at = Column(DateTime, server_default=func.now())

    def __repr__(self):
        return f"<Entity(id={self.id}, name='{self.name}', type='{self.type}')>"


class Trend(Base):
    """Trend detection model."""

    __tablename__ = "trends"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text)
    start_date = Column(DateTime, nullable=False)
    peak_date = Column(DateTime)
    end_date = Column(DateTime)
    confidence_score = Column(Float, default=0.0)
    impact_level = Column(String(50), default="low")  # low, medium, high
    keywords = Column(JSON, default=list)
    created_at = Column(DateTime, server_default=func.now())

    def __repr__(self):
        return f"<Trend(id={self.id}, name='{self.name}', confidence={self.confidence_score})>"


class Node(Base):
    """Graph node for network analysis."""

    __tablename__ = "graph_nodes"

    id = Column(Integer, primary_key=True, index=True)
    node_id = Column(String(255), nullable=False, unique=True, index=True)
    node_type = Column(String(50), nullable=False, index=True)  # article, entity, person, etc.
    properties = Column(JSON, default=dict)
    created_at = Column(DateTime, server_default=func.now())

    def __repr__(self):
        return f"<Node(id={self.id}, node_id='{self.node_id}', type='{self.node_type}')>"


class Edge(Base):
    """Graph edge for relationship analysis."""

    __tablename__ = "graph_edges"

    id = Column(Integer, primary_key=True, index=True)
    source_id = Column(String(255), nullable=False, index=True)
    target_id = Column(String(255), nullable=False, index=True)
    relationship_type = Column(String(100), nullable=False, index=True)
    strength = Column(Float, default=1.0)
    confidence = Column(Float, default=1.0)
    properties = Column(JSON, default=dict)
    created_at = Column(DateTime, server_default=func.now())

    def __repr__(self):
        return f"<Edge(id={self.id}, source='{self.source_id}', target='{self.target_id}', type='{self.relationship_type}')>"