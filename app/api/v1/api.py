"""
ARAS Microservice API Router
Main API router for all endpoints

Built by Elite Team - Backend Developers (PhD in Software Engineering)
"""

from fastapi import APIRouter

from app.api.v1.endpoints import analysis, articles, entities, health, trends

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(articles.router, prefix="/articles", tags=["articles"])
api_router.include_router(entities.router, prefix="/entities", tags=["entities"])
api_router.include_router(trends.router, prefix="/trends", tags=["trends"])
api_router.include_router(analysis.router, prefix="/analysis", tags=["analysis"])
