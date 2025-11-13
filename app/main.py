"""
ARAS Microservice - Main FastAPI Application
Advanced News Analysis System

Built by Elite Team:
- Software Architect: PhD in Computer Science
- Backend Developers: PhD in Software Engineering
- Data Scientist: PhD in Data Science
- Security Specialist: PhD in Cybersecurity
- QA Engineer: PhD in Software Testing

Features:
- News ingestion from RSS/Web/APIs
- NLP processing (spaCy/Hazm)
- Graph analytics (NetworkX)
- Trend detection
- Entity extraction
- Sentiment analysis
- Topic modeling
"""

import logging
import time
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse

from app.api.v1.api import api_router
from app.core.config import settings
from app.core.database import create_tables
from app.core.rate_limiter import RateLimiter
from app.core.redis_client import redis_client
from app.core.security_headers import SecurityHeadersMiddleware
from app.core.audit_logger import AuditLoggerMiddleware

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan context manager."""
    logger.info("Starting ARAS Microservice...")

    # Startup
    await create_tables()
    await redis_client.connect()

    logger.info("ARAS Microservice started successfully")

    yield

    # Shutdown
    await redis_client.disconnect()
    logger.info("ARAS Microservice shut down")


# Create FastAPI app
app = FastAPI(
    title="ARAS Microservice",
    description="Advanced News Analysis System - Reusable Microservice",
    version="1.0.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# Set up CORS
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Add security headers middleware
app.add_middleware(SecurityHeadersMiddleware)

# Add audit logging middleware
app.add_middleware(AuditLoggerMiddleware)

# Add trusted host middleware
if not settings.DEBUG:
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=settings.ALLOWED_HOSTS,
    )


# Rate limiting middleware
rate_limiter = RateLimiter(requests_per_minute=60, requests_per_hour=1000)


@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    """Apply rate limiting to all requests."""
    # Skip rate limiting for health check
    if request.url.path in ["/health", "/"]:
        return await call_next(request)

    # Check rate limit
    try:
        await rate_limiter.check_rate_limit(request)
    except Exception as e:
        # If rate limit exceeded, exception is already raised
        # If Redis error, log and continue
        if "Rate limit exceeded" not in str(e):
            logger.warning(f"Rate limiting error: {e}")

    # Add request timing
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time

    # Add headers
    response.headers["X-Process-Time"] = str(process_time)
    if hasattr(request.state, "rate_limit_remaining_minute"):
        response.headers["X-RateLimit-Remaining-Minute"] = str(
            request.state.rate_limit_remaining_minute
        )
        response.headers["X-RateLimit-Remaining-Hour"] = str(
            request.state.rate_limit_remaining_hour
        )

    return response


@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring."""
    return {"status": "healthy", "service": "ARAS Microservice"}


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "ARAS Microservice - Advanced News Analysis System",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
    }


# Include API router
app.include_router(api_router, prefix=settings.API_V1_STR)


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info",
    )
