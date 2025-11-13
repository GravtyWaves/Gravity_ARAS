"""
Health Check Endpoint
Monitoring and health checks

Built by Elite Team - DevOps Engineer (PhD in Distributed Systems)
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.redis_client import redis_client
from app.schemas.news_schemas import APIResponse

router = APIRouter()


@router.get("/", response_model=APIResponse)
async def health_check(db: AsyncSession = Depends(get_db)):
    """Comprehensive health check for all services."""
    health_status = {"database": False, "redis": False, "overall": False}

    # Check database
    try:
        await db.execute("SELECT 1")
        health_status["database"] = True
    except Exception:
        pass

    # Check Redis
    try:
        await redis_client.client.ping()
        health_status["redis"] = True
    except Exception:
        pass

    # Overall health
    health_status["overall"] = health_status["database"] and health_status["redis"]

    return APIResponse(
        success=health_status["overall"], message="Health check completed", data=health_status
    )


@router.get("/database", response_model=APIResponse)
async def database_health(db: AsyncSession = Depends(get_db)):
    """Database-specific health check."""
    try:
        await db.execute("SELECT 1")
        return APIResponse(success=True, message="Database connection healthy")
    except Exception as e:
        return APIResponse(success=False, message=f"Database connection failed: {str(e)}")


@router.get("/redis", response_model=APIResponse)
async def redis_health():
    """Redis-specific health check."""
    try:
        await redis_client.client.ping()
        return APIResponse(success=True, message="Redis connection healthy")
    except Exception as e:
        return APIResponse(success=False, message=f"Redis connection failed: {str(e)}")
