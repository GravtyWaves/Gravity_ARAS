"""
Articles API Endpoints
CRUD operations for news articles

Built by Elite Team - Backend Developers (PhD in Software Engineering)
"""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.news_schemas import APIResponse, NewsArticle, NewsArticleCreate, NewsArticleUpdate
from app.services.news_service import NewsService

router = APIRouter()


@router.post("/", response_model=APIResponse)
async def create_article(article: NewsArticleCreate, db: AsyncSession = Depends(get_db)):
    """Create a new news article."""
    try:
        created_article = await NewsService.create_article(db, article)
        return APIResponse(
            success=True,
            message="Article created successfully",
            data={"article": NewsArticle.from_orm(created_article).model_dump()},
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create article: {str(e)}")


@router.get("/{article_id}", response_model=APIResponse)
async def get_article(article_id: int, db: AsyncSession = Depends(get_db)):
    """Get a specific news article by ID."""
    article = await NewsService.get_article_by_id(db, article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")

    return APIResponse(
        success=True,
        message="Article retrieved successfully",
        data={"article": NewsArticle.from_orm(article).model_dump()},
    )


@router.get("/", response_model=APIResponse)
async def get_articles(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    category: Optional[str] = Query(None, description="Filter by category"),
    source: Optional[str] = Query(None, description="Filter by source"),
    language: Optional[str] = Query(None, description="Filter by language (e.g., 'en', 'fa')"),
    start_date: Optional[str] = Query(
        None, description="Filter by published_date >= start_date (ISO format)"
    ),
    end_date: Optional[str] = Query(
        None, description="Filter by published_date <= end_date (ISO format)"
    ),
    sort_by: str = Query("published_date", description="Field to sort by"),
    sort_order: str = Query(
        "desc", regex="^(asc|desc)$", description="Sort order: 'asc' or 'desc'"
    ),
    db: AsyncSession = Depends(get_db),
):
    """
    Get list of news articles with filtering, sorting, and pagination.

    Supports:
    - Pagination: skip, limit
    - Filtering: category, source, language, date range
    - Sorting: sort_by, sort_order
    """
    articles = await NewsService.get_articles(
        db=db,
        skip=skip,
        limit=limit,
        category=category,
        source=source,
        language=language,
        start_date=start_date,
        end_date=end_date,
        sort_by=sort_by,
        sort_order=sort_order,
    )

    return APIResponse(
        success=True,
        message=f"Retrieved {len(articles)} articles",
        data={
            "articles": [NewsArticle.from_orm(article).model_dump() for article in articles],
            "total": len(articles),
            "skip": skip,
            "limit": limit,
            "filters": {
                "category": category,
                "source": source,
                "language": language,
                "start_date": start_date,
                "end_date": end_date,
            },
            "sorting": {"sort_by": sort_by, "sort_order": sort_order},
        },
    )


@router.put("/{article_id}", response_model=APIResponse)
async def update_article(
    article_id: int, article_update: NewsArticleUpdate, db: AsyncSession = Depends(get_db)
):
    """Update an existing news article."""
    updated_article = await NewsService.update_article(db, article_id, article_update)
    if not updated_article:
        raise HTTPException(status_code=404, detail="Article not found")

    return APIResponse(
        success=True,
        message="Article updated successfully",
        data={"article": NewsArticle.from_orm(updated_article).model_dump()},
    )


@router.delete("/{article_id}", response_model=APIResponse)
async def delete_article(article_id: int, db: AsyncSession = Depends(get_db)):
    """Delete a news article."""
    deleted = await NewsService.delete_article(db, article_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Article not found")

    return APIResponse(success=True, message="Article deleted successfully")


@router.get("/search/", response_model=APIResponse)
async def search_articles(
    q: str = Query(..., min_length=1, max_length=100),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: AsyncSession = Depends(get_db),
):
    """Search articles by title or content."""
    articles = await NewsService.search_articles(db, q, skip, limit)

    return APIResponse(
        success=True,
        message=f"Found {len(articles)} articles matching '{q}'",
        data={
            "articles": [NewsArticle.from_orm(article).model_dump() for article in articles],
            "query": q,
            "total": len(articles),
        },
    )
