# ARAS Microservice

[![Python Version](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green.svg)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Test Coverage](https://img.shields.io/badge/coverage-67%25-yellow.svg)](https://github.com/GravtyWaves/Gravity_ARAS)
[![Security: Bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)

Advanced Reusable Analysis System (ARAS) - A high-performance microservice for intelligent news analysis with multi-language support (Persian/English), entity extraction, sentiment analysis, and trend detection.

## 🚀 Features

### Core Capabilities
- **🌍 Multi-language Support**: Native Persian (Farsi) and English text processing
- **🔍 Full-Text Search**: PostgreSQL-powered search with relevance ranking (`ts_rank`)
- **🧠 Advanced NLP**: Sentiment analysis, entity extraction, topic modeling (upcoming)
- **📊 Graph Analysis**: Entity relationship networks and centrality measures (upcoming)
- **⚡ High Performance**: Async I/O, Redis caching, connection pooling
- **🛡️ Rate Limiting**: Three-tier protection (strict/moderate/relaxed)
- **🔐 Security**: Input validation, SQL injection prevention, Bandit-scanned code

### API Features
- **RESTful Design**: Well-structured endpoints with versioning (`/api/v1/`)
- **Advanced Filtering**: Multi-criteria search (category, source, language, tags, sentiment, dates)
- **Pagination**: Efficient data retrieval with `skip`/`limit` parameters
- **OpenAPI Documentation**: Interactive Swagger UI and ReDoc
- **Health Monitoring**: Database and Redis connectivity checks
- **Error Handling**: Standardized error responses with detailed messages

### Infrastructure
- **Database**: PostgreSQL 16 with full-text search (GIN indexes)
- **Cache**: Redis 7.x for rate limiting and caching
- **Containerization**: Docker and Docker Compose ready
- **Orchestration**: Kubernetes manifests for staging/production
- **Testing**: pytest with 67% coverage, asyncio support
- **CI/CD**: GitHub Actions pipeline (lint, test, build, security, deploy)

## 📊 Current Status (Sprint 1 - 90% Complete)

**Completed:**
- ✅ Full-text search with PostgreSQL tsvector
- ✅ Advanced filtering API endpoints
- ✅ Rate limiting middleware (60/min, 1000/hr)
- ✅ Test coverage: 67% (exceeded 60% target)
- ✅ Security audit: Bandit scan passed
- ✅ Kubernetes deployment manifests
- ✅ Complete documentation (API, Architecture, K8s)

**In Progress:**
- 🔄 Sprint 2: NLP integration (Hazm for Persian, spaCy for English)
- 🔄 Entity extraction (85%/90% accuracy targets)
- 🔄 Sentiment analysis (80%/85% accuracy targets)

**Upcoming:**
- 📅 Graph analysis with NetworkX
- 📅 Data ingestion with Scrapy (30 news sources)
- 📅 Production deployment (Target: Jan 31, 2026)

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────┐
│              External Clients                        │
│         (Web Apps, Mobile Apps, APIs)               │
└──────────────────┬──────────────────────────────────┘
                   │
                   ▼
          ┌────────────────┐
          │  Load Balancer │
          │   (Nginx/K8s)  │
          └────────┬───────┘
                   │
                   ▼
       ┌───────────────────────┐
       │  FastAPI Application  │
       │   (Async ASGI Server) │
       └───────────┬───────────┘
                   │
      ┌────────────┼────────────┐
      │            │            │
      ▼            ▼            ▼
┌──────────┐ ┌──────────┐ ┌──────────┐
│   API    │ │ Service  │ │   NLP    │
│  Layer   │ │  Layer   │ │  Engine  │
└──────────┘ └──────────┘ └──────────┘
      │            │            │
      └────────────┼────────────┘
                   │
      ┌────────────┴────────────┐
      │                         │
      ▼                         ▼
┌──────────────┐      ┌──────────────┐
│  PostgreSQL  │      │    Redis     │
│  (Primary)   │      │  (Cache/RL)  │
│              │      │              │
│ - Articles   │      │ - Limits     │
│ - Entities   │      │ - Cache      │
│ - Trends     │      │ - Sessions   │
│ - FTS Index  │      │              │
└──────────────┘      └──────────────┘
```

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for detailed architecture documentation.

## 📋 Prerequisites

- **Python 3.12+** (tested on 3.12.1)
- **PostgreSQL 16** (for production) or SQLite (for development/testing)
- **Redis 7.x** (optional, for caching and rate limiting)
- **Docker & Docker Compose** (for containerized deployment)
- **Kubernetes** (optional, for staging/production deployment)

## 🛠️ Installation

### Quick Start with Docker (Recommended)

```bash
# Clone the repository
git clone https://github.com/GravtyWaves/Gravity_ARAS.git
cd Gravity_ARAS

# Start all services
docker-compose up --build

# Access the API
open http://localhost:8000/docs
```

That's it! The API, PostgreSQL, and Redis are now running.

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/GravtyWaves/Gravity_ARAS.git
   cd Gravity_ARAS
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -e ".[dev]"  # Includes dev dependencies (pytest, black, etc.)
   ```

4. **Set up environment variables**
   ```bash
   # Create .env file (or use environment variables)
   cat > .env << EOF
   DATABASE_URL=postgresql+asyncpg://aras_user:aras_password@localhost:5432/aras_db
   REDIS_HOST=localhost
   REDIS_PORT=6379
   ENVIRONMENT=development
   LOG_LEVEL=INFO
   EOF
   ```

5. **Start PostgreSQL and Redis** (if not using Docker)
   ```bash
   # PostgreSQL
   sudo systemctl start postgresql
   createdb aras_db
   createuser aras_user
   
   # Redis
   sudo systemctl start redis
   ```

6. **Run database migrations**
   ```bash
   alembic upgrade head
   ```

7. **Start the application**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

8. **Verify installation**
   ```bash
   curl http://localhost:8000/health
   # Expected: {"success": true, "data": {"status": "healthy", ...}}
   ```

### Kubernetes Deployment

See [k8s/README.md](k8s/README.md) for detailed Kubernetes deployment instructions.

```bash
# Quick deployment to staging
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/secret.yaml  # Update secrets first!
kubectl apply -f k8s/postgresql.yaml
kubectl apply -f k8s/redis.yaml
kubectl apply -f k8s/deployment.yaml
```

## 📖 API Documentation

### Interactive Documentation

Once the application is running, visit:
- **Swagger UI**: http://localhost:8000/docs (interactive API testing)
- **ReDoc**: http://localhost:8000/redoc (clean documentation)
- **OpenAPI Schema**: http://localhost:8000/openapi.json (machine-readable)

### Comprehensive Guides

- **[API Documentation](docs/API.md)**: Complete endpoint reference with examples
- **[Architecture Guide](docs/ARCHITECTURE.md)**: System design and data flow
- **[Deployment Guide](docs/DEPLOYMENT.md)**: Production deployment instructions
- **[Kubernetes Guide](k8s/README.md)**: K8s deployment and operations

### Key Endpoints

#### Health & Status
```http
GET /health
```
**Response:** Database and Redis connectivity status

#### Articles Management
```http
POST   /api/v1/articles/                    # Create article
GET    /api/v1/articles/?skip=0&limit=10    # List articles (paginated)
GET    /api/v1/articles/{id}                # Get article by ID
PUT    /api/v1/articles/{id}                # Update article
DELETE /api/v1/articles/{id}                # Delete article
```

#### Search (New in Sprint 1)
```http
# Basic full-text search
GET /api/v1/articles/search/?q=climate+change&language=en&limit=20

# Advanced multi-filter search
POST /api/v1/articles/search/advanced
Content-Type: application/json

{
  "q": "climate change",
  "category": "environment",
  "source": "BBC News",
  "language": "en",
  "tags": ["climate", "policy"],
  "sentiment_min": 0.3,
  "sentiment_max": 0.8,
  "start_date": "2025-01-01T00:00:00Z",
  "end_date": "2025-12-31T23:59:59Z",
  "skip": 0,
  "limit": 20
}
```

#### Analysis Endpoints
```http
POST /api/v1/analysis/sentiment   # Sentiment analysis (positive/neutral/negative)
POST /api/v1/analysis/entities    # Entity extraction (PERSON, ORG, LOCATION)
POST /api/v1/analysis/topics      # Topic modeling (upcoming)
POST /api/v1/analysis/graph       # Graph analysis (upcoming)
POST /api/v1/analysis/batch       # Batch processing (max 50 texts)
```

#### Entities & Trends
```http
GET    /api/v1/entities/?skip=0&limit=10       # List entities
GET    /api/v1/entities/{id}                   # Get entity by ID
GET    /api/v1/entities/search/?query=Tesla    # Search entities
GET    /api/v1/trends/?skip=0&limit=10         # List trends
GET    /api/v1/trends/active/                  # Active trends only
GET    /api/v1/trends/{id}                     # Get trend by ID
```

### Rate Limits

API implements three-tier rate limiting:

| Tier | Endpoints | Limits |
|------|-----------|--------|
| **Strict** | `/api/v1/analysis/batch` | 10 req/min, 200 req/hr |
| **Moderate** | `/api/v1/articles/search/advanced`, `/api/v1/analysis/graph` | 30 req/min, 500 req/hr |
| **Relaxed** | All other endpoints | 100 req/min, 1000 req/hr |

Rate limit headers in responses:
```http
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1699876543
X-RateLimit-Window: 60
```

## 🧪 Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=app --cov-report=term --cov-report=html

# Run specific test file
pytest tests/test_articles.py

# Run specific test
pytest tests/test_health.py::test_health_check

# Run with verbose output
pytest -v

# Run only async tests
pytest -m asyncio
```

### Current Test Coverage

**Overall: 67%** (903 statements, 297 missing)

| Module | Coverage |
|--------|----------|
| `app/main.py` | 90% |
| `app/models/news_models.py` | 100% |
| `app/schemas/news_schemas.py` | 100% |
| `app/services/analysis_service.py` | 70% |
| `app/services/news_service.py` | 67% |

### Test Suites

- **Health Tests** (10 tests): API health checks, database connectivity, performance
- **Articles Tests** (18 tests): CRUD operations, validation, pagination, search
- **Analysis Tests** (12 tests): Sentiment, entities, topics, batch processing
- **Entities & Trends Tests** (12 tests): List, filter, search, pagination
- **Search Tests**: Full-text search, advanced filtering
- **Rate Limiting Tests**: Multi-tier rate limiting, Redis fallback
- **Service Tests**: News service, analysis service unit tests

## 🛡️ Security

### Security Measures

- **Input Validation**: All inputs validated with Pydantic schemas
- **SQL Injection Prevention**: SQLAlchemy ORM with parameterized queries
- **Rate Limiting**: DDoS protection with three-tier limits
- **CORS Configuration**: Configurable allowed origins
- **Environment Variables**: Secrets managed via environment variables
- **Security Scanning**: Bandit static analysis (0 high severity issues)

### Security Audit Results (Bandit)

```
Total lines scanned: 1,683
High severity issues: 0
Medium severity issues: 1 (bind to 0.0.0.0 - expected for dev)
Low severity issues: 2 (try-except-pass - acceptable)
Overall: PASS ✓
```

### Best Practices

- Never commit `.env` files or secrets to version control
- Use strong, randomly generated passwords for PostgreSQL and Redis
- Enable SSL/TLS for production deployments
- Rotate credentials regularly
- Use Kubernetes Secrets or external secret managers (Vault, AWS Secrets Manager) for production

## 🔧 Configuration

### Environment Variables

The application uses environment variables for configuration:

```env
# Application
APP_NAME=ARAS Microservice
ENVIRONMENT=development  # development, staging, production
LOG_LEVEL=INFO

# Database (PostgreSQL)
DATABASE_URL=postgresql+asyncpg://aras_user:aras_password@localhost:5432/aras_db
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=aras_db
POSTGRES_USER=aras_user
POSTGRES_PASSWORD=aras_password

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
REDIS_PASSWORD=  # Optional

# API Settings
API_V1_PREFIX=/api/v1
CORS_ORIGINS=["http://localhost:3000", "http://localhost:8000"]

# Rate Limiting
RATE_LIMIT_ENABLED=true
RATE_LIMIT_PER_MINUTE=100
RATE_LIMIT_PER_HOUR=1000

# Cache
CACHE_ENABLED=true
CACHE_TTL_SECONDS=300

# NLP Settings
NLP_BATCH_SIZE=32
NLP_MAX_LENGTH=5000
```

### Configuration Files

- **`app/core/config.py`**: Application configuration class
- **`alembic.ini`**: Database migration configuration
- **`docker-compose.yml`**: Docker services configuration
- **`pyproject.toml`**: Python project metadata and dependencies

## 🚀 Development

### Code Quality

This project maintains high code quality standards:

```bash
# Format code with Black
black app/ tests/

# Sort imports with isort
isort app/ tests/

# Lint with Flake8
flake8 app/ tests/

# Type check with mypy (optional)
mypy app/

# Security scan with Bandit
bandit -r app/ -f txt -o security_report.txt

# Run all checks
./scripts/lint.sh
```

### Pre-commit Hooks

Install pre-commit hooks to enforce standards:

```bash
pip install pre-commit
pre-commit install

# Run manually
pre-commit run --all-files
```

### Database Migrations

```bash
# Create a new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1

# View migration history
alembic history

# View current version
alembic current
```

### Seed Data

Generate test data for development:

```bash
# Run seed data script (requires PostgreSQL)
python scripts/seed_data.py

# This creates:
# - 100+ articles (Persian and English)
# - 50+ entities
# - 20+ trends
# - Graph relationships
```
SPACY_MODEL_EN=en_core_web_sm
SPACY_MODEL_FA=fa

# Application
DEBUG=True
API_V1_STR=/api/v1
```

## 🚀 Deployment

### Production Deployment

1. **Build production image**
   ```bash
   docker build -t aras-microservice:latest .
   ```

2. **Run with production compose**
   ```bash
   docker-compose -f docker-compose.prod.yml up -d
   ```

3. **Scale the application**
   ```bash
   docker-compose up -d --scale aras-app=3
   ```

### Kubernetes Deployment

Use the provided Kubernetes manifests in the `k8s/` directory:

```bash
kubectl apply -f k8s/
```

## 📊 Monitoring

### Health Checks

The service provides comprehensive health checks:

```json
{
  "success": true,
  "data": {
    "status": "healthy",
    "timestamp": "2024-01-01T00:00:00Z",
    "version": "1.0.0",
    "database": {
      "status": "connected"
    },
    "redis": {
      "status": "connected"
    }
  }
}
```

### Logging

Structured logging with JSON format for production monitoring.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Team

Built by the ARAS Elite Team - PhD-level researchers and developers specializing in AI, NLP, and distributed systems.

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/aras-team/aras-microservice/issues)
- **Documentation**: [Wiki](https://github.com/aras-team/aras-microservice/wiki)
- **Discussions**: [GitHub Discussions](https://github.com/aras-team/aras-microservice/discussions)

## 🔄 Roadmap

- [ ] Real-time streaming analysis
- [ ] Advanced ML model integration
- [ ] Multi-modal content analysis
- [ ] Distributed processing with Apache Kafka
- [ ] Graph database integration
- [ ] Advanced visualization dashboard

---

**ARAS**: Advanced Reusable Analysis System - Transforming news analysis through intelligent microservices.