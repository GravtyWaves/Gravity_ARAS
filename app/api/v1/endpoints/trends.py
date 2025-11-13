"""
Trends API Endpoints
CRUD operations for trend detection

Built by Elite Team - Backend Developers (PhD in Software Engineering)
"""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.news_models import Trend
from app.schemas.news_schemas import APIResponse
from app.schemas.news_schemas import Trend as TrendSchema
from app.schemas.news_schemas import TrendCreate, TrendUpdate

router = APIRouter()


@router.post("/", response_model=APIResponse)
async def create_trend(trend: TrendCreate, db: AsyncSession = Depends(get_db)):
    """Create a new trend."""
    try:
        db_trend = Trend(**trend.model_dump())
        db.add(db_trend)
        await db.commit()
        await db.refresh(db_trend)

        return APIResponse(
            success=True,
            message="Trend created successfully",
            data={"trend": TrendSchema.from_orm(db_trend).model_dump()},
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create trend: {str(e)}")


@router.get("/{trend_id}", response_model=APIResponse)
async def get_trend(trend_id: int, db: AsyncSession = Depends(get_db)):
    """Get a specific trend by ID."""
    result = await db.execute(select(Trend).where(Trend.id == trend_id))
    trend = result.scalar_one_or_none()

    if not trend:
        raise HTTPException(status_code=404, detail="Trend not found")

    return APIResponse(
        success=True,
        message="Trend retrieved successfully",
        data={"trend": TrendSchema.from_orm(trend).model_dump()},
    )


@router.get("/", response_model=APIResponse)
async def get_trends(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    impact_level: Optional[str] = Query(
        None, description="Filter by impact level (low, medium, high)"
    ),
    min_confidence: float = Query(0.0, ge=0.0, le=1.0, description="Minimum confidence score"),
    start_date: Optional[str] = Query(
        None, description="Filter by start_date >= start_date (ISO format)"
    ),
    end_date: Optional[str] = Query(
        None, description="Filter by start_date <= end_date (ISO format)"
    ),
    sort_by: str = Query("confidence_score", description="Field to sort by"),
    sort_order: str = Query(
        "desc", regex="^(asc|desc)$", description="Sort order: 'asc' or 'desc'"
    ),
    db: AsyncSession = Depends(get_db),
):
    """
    Get list of trends with filtering, sorting, and pagination.

    Supports:
    - Pagination: skip, limit
    - Filtering: impact_level, min_confidence, date range
    - Sorting: sort_by, sort_order
    """
    from datetime import datetime

    query = select(Trend)

    # Apply filters
    if min_confidence > 0.0:
        query = query.where(Trend.confidence_score >= min_confidence)
    if impact_level:
        query = query.where(Trend.impact_level == impact_level)
    if start_date:
        query = query.where(Trend.start_date >= datetime.fromisoformat(start_date))
    if end_date:
        query = query.where(Trend.start_date <= datetime.fromisoformat(end_date))

    # Apply sorting
    sort_column = getattr(Trend, sort_by, Trend.confidence_score)
    if sort_order.lower() == "asc":
        query = query.order_by(sort_column.asc())
    else:
        query = query.order_by(sort_column.desc())

    # Apply pagination
    query = query.offset(skip).limit(limit)

    result = await db.execute(query)
    trends = result.scalars().all()

    return APIResponse(
        success=True,
        message=f"Retrieved {len(trends)} trends",
        data={
            "trends": [TrendSchema.from_orm(trend).model_dump() for trend in trends],
            "total": len(trends),
            "skip": skip,
            "limit": limit,
            "filters": {
                "impact_level": impact_level,
                "min_confidence": min_confidence,
                "start_date": start_date,
                "end_date": end_date,
            },
            "sorting": {"sort_by": sort_by, "sort_order": sort_order},
        },
    )


@router.put("/{trend_id}", response_model=APIResponse)
async def update_trend(
    trend_id: int, trend_update: TrendUpdate, db: AsyncSession = Depends(get_db)
):
    """Update an existing trend."""
    result = await db.execute(select(Trend).where(Trend.id == trend_id))
    trend = result.scalar_one_or_none()

    if not trend:
        raise HTTPException(status_code=404, detail="Trend not found")

    # Update fields
    update_dict = trend_update.model_dump(exclude_unset=True)
    for field, value in update_dict.items():
        setattr(trend, field, value)

    await db.commit()
    await db.refresh(trend)

    return APIResponse(
        success=True,
        message="Trend updated successfully",
        data={"trend": TrendSchema.from_orm(trend).model_dump()},
    )


@router.delete("/{trend_id}", response_model=APIResponse)
async def delete_trend(trend_id: int, db: AsyncSession = Depends(get_db)):
    """Delete a trend."""
    result = await db.execute(select(Trend).where(Trend.id == trend_id))
    trend = result.scalar_one_or_none()

    if not trend:
        raise HTTPException(status_code=404, detail="Trend not found")

    await db.delete(trend)
    await db.commit()

    return APIResponse(success=True, message="Trend deleted successfully")


@router.get("/active/", response_model=APIResponse)
async def get_active_trends(db: AsyncSession = Depends(get_db)):
    """Get currently active trends (no end_date)."""
    result = await db.execute(
        select(Trend).where(Trend.end_date.is_(None)).order_by(Trend.confidence_score.desc())
    )
    trends = result.scalars().all()

    return APIResponse(
        success=True,
        message=f"Retrieved {len(trends)} active trends",
        data={
            "trends": [TrendSchema.from_orm(trend).model_dump() for trend in trends],
            "total": len(trends),
        },
    )
