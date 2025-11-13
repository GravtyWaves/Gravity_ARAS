# Changelog

All notable changes to the ARAS Microservice will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Sprint 2 (NLP Integration) - Planned
- Hazm integration for Persian text processing
- spaCy integration for English NER and analysis
- Gensim integration for topic modeling
- Entity extraction with 85%/90% accuracy targets
- Sentiment analysis with 80%/85% accuracy targets
- Graph analysis with NetworkX
- Data ingestion with Scrapy (30 sources)

---

## [0.2.0] - 2025-11-13 - Sprint 1 Complete (90%)

### Added

**API Features:**
- Full-text search endpoint (`GET /api/v1/articles/search/`) with PostgreSQL `tsvector` and `ts_rank`
- Advanced search endpoint (`POST /api/v1/articles/search/advanced`) with multi-filter support
  - Category, source, language, tags filtering
  - Sentiment range filtering (min/max)
  - Date range filtering (start/end)
  - Pagination with skip/limit
- Rate limiting middleware with three tiers:
  - Strict: 10 req/min, 200 req/hr (batch analysis)
  - Moderate: 30 req/min, 500 req/hr (advanced search)
  - Relaxed: 100 req/min, 1000 req/hr (standard endpoints)
- Rate limit headers in all responses (X-RateLimit-*)

**Database:**
- Full-text search migration (`c2352ab4b554`):
  - Added `search_vector` tsvector column to news_articles
  - Created GIN index for full-text search performance
  - Added URL uniqueness constraint
  - Implemented automatic search_vector updates via triggers

**Infrastructure:**
- Redis-based rate limiting with graceful degradation (optional Redis)
- Redis caching layer with configurable TTL
- Comprehensive test suite (67% coverage):
  - 18 article endpoint tests
  - 10 health check tests
  - 12 analysis endpoint tests
  - 12 entity/trend tests
  - Rate limiting tests
  - Search functionality tests
  - News service tests
- Security audit with Bandit (0 high severity issues)
- Seed data generator script for development (100+ articles, 50+ entities, 20+ trends)

**Documentation:**
- Complete API documentation with examples (docs/API.md)
- System architecture documentation (docs/ARCHITECTURE.md)
- Kubernetes deployment manifests (k8s/)
  - Namespace, ConfigMap, Secret configurations
  - PostgreSQL StatefulSet with persistent storage
  - Redis StatefulSet with persistent storage
  - API Deployment with HPA (2-5 replicas)
  - Ingress with SSL/TLS support
  - NetworkPolicy for pod security
  - Database migration and seed jobs
  - CronJob for periodic tasks
- Kubernetes deployment guide (k8s/README.md)

**Code Quality:**
- Black formatting (line-length 100)
- isort import sorting (black profile)
- Flake8 linting (0 errors)
- Conventional commit messages

### Changed
- Redis connection errors are now warnings instead of fatal errors
- Application can run without Redis (caching disabled)
- Test suite uses SQLite by default (PostgreSQL optional)
- Improved error handling for optional services

### Fixed
- Redis connection failures no longer crash the application
- Rate limiting works with or without Redis
- Test suite compatibility with both SQLite and PostgreSQL

### Security
- Bandit security scan passed (0 high, 1 medium, 2 low severity)
- Input validation with Pydantic on all endpoints
- SQL injection prevention with SQLAlchemy ORM
- Rate limiting for DDoS protection
- Environment-based secret management

### Performance
- Full-text search with GIN indexes (10-100x faster than LIKE queries)
- Redis caching for frequently accessed data
- Connection pooling for database
- Async I/O throughout the stack

### Testing
- Test coverage: 67% (903 statements, 297 missing)
- Coverage by module:
  - app/main.py: 90%
  - app/models/news_models.py: 100%
  - app/schemas/news_schemas.py: 100%
  - app/services/analysis_service.py: 70%
  - app/services/news_service.py: 67%
- All tests passing with pytest
- Integration tests for API endpoints
- Unit tests for services and models

---

## [0.1.0] - 2025-11-11 - Initial Project Setup

### Added
- Complete project structure and initial setup
- Core API endpoints (Health, Articles, Entities, Trends, Analysis)
- SQLAlchemy models for news articles, entities, trends, and graph data
- Pydantic schemas for request/response validation
- Database configuration with async SQLAlchemy
- Redis client for caching
- Docker and Docker Compose setup
- Basic test suite with pytest
- CI/CD pipeline structure with GitHub Actions
- Documentation structure (API, Deployment, TODO)
- Shell scripts for common tasks (init_db, start_dev, run_tests, lint)
- Alembic migration system
- Initial database migration (278207100710)

### Changed
- Nothing yet

### Deprecated
- Nothing yet

### Removed
- Nothing yet

### Fixed
- Nothing yet

### Security
- Environment-based configuration
- Input validation with Pydantic
- SQL injection prevention with parametrized queries

---

## [1.0.0] - Target: 2026-01-31

### Planned Features
- Complete NLP processing (Persian with Hazm, English with spaCy)
- Entity extraction with 90%+ accuracy
- Sentiment analysis with 85%+ accuracy
- Topic modeling with Gensim LDA
- Graph analysis with NetworkX
- Community detection and centrality measures
- Trend detection and forecasting
- Data ingestion with Scrapy
- Background task processing with Celery
- Comprehensive test suite with 95%+ coverage
- Production-ready deployment configuration
- Complete API and user documentation

---

## Version History

### Version 0.1.0 - 2025-11-13 (Development Start)
- Initial project structure
- Core infrastructure setup
- Basic API implementation

---

**Note:** This changelog will be updated regularly as features are completed and released.
