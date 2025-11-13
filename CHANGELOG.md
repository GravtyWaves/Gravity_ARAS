# Changelog

All notable changes to the ARAS Microservice will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Complete project structure and initial setup
- Core API endpoints (Health, Articles, Entities, Trends, Analysis)
- SQLAlchemy models for news articles, entities, trends, and graph data
- Pydantic schemas for request/response validation
- Database configuration with async SQLAlchemy
- Redis client for caching
- Docker and Docker Compose setup
- Basic test suite with pytest
- CI/CD pipeline structure
- Documentation structure (API, Deployment, TODO)
- Shell scripts for common tasks (init_db, start_dev, run_tests, lint)

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

## [1.0.0] - Target: 2025-12-31

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
