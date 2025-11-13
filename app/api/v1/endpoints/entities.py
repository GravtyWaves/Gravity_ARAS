"""
Entities API Endpoints
CRUD operations for named entities

Built by Elite Team - Backend Developers (PhD in Software Engineering)
"""

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.news_models import Entity
from app.schemas.news_schemas import (
    APIResponse,
    Entity as EntitySchema,
    EntityCreate,
    EntityUpdate
)

router = APIRouter()


@router.post("/", response_model=APIResponse)
async def create_entity(
    entity: EntityCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a new named entity."""
    try:
        # Check for duplicate name
        existing = await db.execute(
            select(Entity).where(Entity.name == entity.name, Entity.type == entity.type)
        )
        if existing.scalar_one_or_none():
            raise ValueError("Entity with this name and type already exists")

        db_entity = Entity(**entity.model_dump())
        db.add(db_entity)
        await db.commit()
        await db.refresh(db_entity)

        return APIResponse(
            success=True,
            message="Entity created successfully",
            data={"entity": EntitySchema.from_orm(db_entity).model_dump()}
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create entity: {str(e)}")


@router.get("/{entity_id}", response_model=APIResponse)
async def get_entity(
    entity_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get a specific entity by ID."""
    result = await db.execute(select(Entity).where(Entity.id == entity_id))
    entity = result.scalar_one_or_none()

    if not entity:
        raise HTTPException(status_code=404, detail="Entity not found")

    return APIResponse(
        success=True,
        message="Entity retrieved successfully",
        data={"entity": EntitySchema.from_orm(entity).model_dump()}
    )


@router.get("/", response_model=APIResponse)
async def get_entities(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    entity_type: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """Get list of entities with optional filtering."""
    query = select(Entity).offset(skip).limit(limit)

    if entity_type:
        query = query.where(Entity.type == entity_type)

    query = query.order_by(Entity.name)

    result = await db.execute(query)
    entities = result.scalars().all()

    return APIResponse(
        success=True,
        message=f"Retrieved {len(entities)} entities",
        data={
            "entities": [EntitySchema.from_orm(entity).model_dump() for entity in entities],
            "total": len(entities),
            "skip": skip,
            "limit": limit
        }
    )


@router.put("/{entity_id}", response_model=APIResponse)
async def update_entity(
    entity_id: int,
    entity_update: EntityUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update an existing entity."""
    result = await db.execute(select(Entity).where(Entity.id == entity_id))
    entity = result.scalar_one_or_none()

    if not entity:
        raise HTTPException(status_code=404, detail="Entity not found")

    # Update fields
    update_dict = entity_update.model_dump(exclude_unset=True)
    for field, value in update_dict.items():
        setattr(entity, field, value)

    await db.commit()
    await db.refresh(entity)

    return APIResponse(
        success=True,
        message="Entity updated successfully",
        data={"entity": EntitySchema.from_orm(entity).model_dump()}
    )


@router.delete("/{entity_id}", response_model=APIResponse)
async def delete_entity(
    entity_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Delete an entity."""
    result = await db.execute(select(Entity).where(Entity.id == entity_id))
    entity = result.scalar_one_or_none()

    if not entity:
        raise HTTPException(status_code=404, detail="Entity not found")

    await db.delete(entity)
    await db.commit()

    return APIResponse(
        success=True,
        message="Entity deleted successfully"
    )


@router.get("/search/", response_model=APIResponse)
async def search_entities(
    q: str = Query(..., min_length=1, max_length=100),
    entity_type: Optional[str] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: AsyncSession = Depends(get_db)
):
    """Search entities by name."""
    query = select(Entity).where(Entity.name.ilike(f"%{q}%")).offset(skip).limit(limit)

    if entity_type:
        query = query.where(Entity.type == entity_type)

    query = query.order_by(Entity.name)

    result = await db.execute(query)
    entities = result.scalars().all()

    return APIResponse(
        success=True,
        message=f"Found {len(entities)} entities matching '{q}'",
        data={
            "entities": [EntitySchema.from_orm(entity).model_dump() for entity in entities],
            "query": q,
            "total": len(entities)
        }
    )