"""
ARAS Microservice News Service
Business logic for news article management

Built by Elite Team - Backend Developers (PhD in Software Engineering)
"""

import logging
from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.redis_client import redis_client
from app.models.news_models import NewsArticle
from app.schemas.news_schemas import NewsArticleCreate, NewsArticleUpdate

logger = logging.getLogger(__name__)


class NewsService:
    """Service for managing news articles."""

    @staticmethod
    async def create_article(db: AsyncSession, article_data: NewsArticleCreate) -> NewsArticle:
        """Create a new news article."""
        # Check for duplicate URL
        existing = await db.execute(
            select(NewsArticle).where(NewsArticle.url == str(article_data.url))
        )
        if existing.scalar_one_or_none():
            raise ValueError("Article with this URL already exists")

        # Create article
        article = NewsArticle(**article_data.model_dump())
        db.add(article)
        await db.commit()
        await db.refresh(article)

        # Cache the article
        await redis_client.set_json(f"article:{article.id}", article_data.model_dump())

        logger.info(f"Created news article: {article.id}")
        return article

    @staticmethod
    async def get_article_by_id(db: AsyncSession, article_id: int) -> Optional[NewsArticle]:
        """Get article by ID."""
        # Try cache first
        cached = await redis_client.get_json(f"article:{article_id}")
        if cached:
            return NewsArticle(**cached)

        # Query database
        result = await db.execute(select(NewsArticle).where(NewsArticle.id == article_id))
        article = result.scalar_one_or_none()

        # Cache if found
        if article:
            await redis_client.set_json(
                f"article:{article_id}",
                {
                    "id": article.id,
                    "title": article.title,
                    "content": article.content,
                    "summary": article.summary,
                    "source": article.source,
                    "published_date": article.published_date.isoformat(),
                    "language": article.language,
                    "category": article.category,
                    "tags": article.tags,
                    "sentiment_score": article.sentiment_score,
                    "entities": article.entities,
                    "topics": article.topics,
                    "url": article.url,
                    "created_at": article.created_at.isoformat(),
                    "updated_at": article.updated_at.isoformat(),
                },
            )

        return article

    @staticmethod
    async def get_articles(
        db: AsyncSession,
        skip: int = 0,
        limit: int = 100,
        category: Optional[str] = None,
        source: Optional[str] = None,
        language: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        sort_by: str = "published_date",
        sort_order: str = "desc",
    ) -> List[NewsArticle]:
        """
        Get list of articles with filtering and sorting.

        Args:
            db: Database session
            skip: Number of records to skip (pagination)
            limit: Maximum number of records to return
            category: Filter by category
            source: Filter by source
            language: Filter by language
            start_date: Filter by published_date >= start_date (ISO format)
            end_date: Filter by published_date <= end_date (ISO format)
            sort_by: Field to sort by (default: published_date)
            sort_order: Sort order - 'asc' or 'desc' (default: desc)
        """
        from datetime import datetime

        query = select(NewsArticle)

        # Apply filters
        if category:
            query = query.where(NewsArticle.category == category)
        if source:
            query = query.where(NewsArticle.source == source)
        if language:
            query = query.where(NewsArticle.language == language)
        if start_date:
            query = query.where(NewsArticle.published_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.where(NewsArticle.published_date <= datetime.fromisoformat(end_date))

        # Apply sorting
        sort_column = getattr(NewsArticle, sort_by, NewsArticle.published_date)
        if sort_order.lower() == "asc":
            query = query.order_by(sort_column.asc())
        else:
            query = query.order_by(sort_column.desc())

        # Apply pagination
        query = query.offset(skip).limit(limit)

        result = await db.execute(query)
        return result.scalars().all()

    @staticmethod
    async def update_article(
        db: AsyncSession, article_id: int, update_data: NewsArticleUpdate
    ) -> Optional[NewsArticle]:
        """Update an existing article."""
        result = await db.execute(select(NewsArticle).where(NewsArticle.id == article_id))
        article = result.scalar_one_or_none()

        if not article:
            return None

        # Update fields
        update_dict = update_data.model_dump(exclude_unset=True)
        for field, value in update_dict.items():
            setattr(article, field, value)

        await db.commit()
        await db.refresh(article)

        # Update cache
        await redis_client.delete(f"article:{article_id}")

        logger.info(f"Updated news article: {article_id}")
        return article

    @staticmethod
    async def delete_article(db: AsyncSession, article_id: int) -> bool:
        """Delete an article."""
        result = await db.execute(select(NewsArticle).where(NewsArticle.id == article_id))
        article = result.scalar_one_or_none()

        if not article:
            return False

        await db.delete(article)
        await db.commit()

        # Remove from cache
        await redis_client.delete(f"article:{article_id}")

        logger.info(f"Deleted news article: {article_id}")
        return True

    @staticmethod
    async def search_articles(
        db: AsyncSession, query: str, skip: int = 0, limit: int = 50
    ) -> List[NewsArticle]:
        """Search articles by title or content."""
        # Simple text search (PostgreSQL full-text search would be better)
        search_query = f"%{query}%"
        result = await db.execute(
            select(NewsArticle)
            .where(
                (NewsArticle.title.ilike(search_query)) | (NewsArticle.content.ilike(search_query))
            )
            .offset(skip)
            .limit(limit)
            .order_by(NewsArticle.published_date.desc())
        )
        return result.scalars().all()
