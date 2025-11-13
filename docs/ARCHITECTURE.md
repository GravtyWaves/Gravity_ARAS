# ARAS System Architecture

## Overview

ARAS (Advanced Reusable Analysis System) is a microservice-based news analysis platform built with FastAPI, designed for high-performance NLP processing of Persian and English news articles.

---

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                         External Clients                              │
│                    (Web Apps, Mobile Apps, APIs)                      │
└────────────────┬──────────────────────────────────┬──────────────────┘
                 │                                   │
                 ▼                                   ▼
        ┌────────────────┐                  ┌────────────────┐
        │  Load Balancer │                  │   API Gateway  │
        │   (Nginx/K8s)  │                  │  (Rate Limit)  │
        └────────┬───────┘                  └────────┬───────┘
                 │                                   │
                 └───────────────┬───────────────────┘
                                 ▼
                    ┌────────────────────────┐
                    │   FastAPI Application  │
                    │    (main.py - ASGI)    │
                    └────────────┬───────────┘
                                 │
        ┌────────────────────────┼────────────────────────┐
        │                        │                        │
        ▼                        ▼                        ▼
┌───────────────┐      ┌──────────────────┐     ┌──────────────┐
│  API Layer    │      │  Service Layer   │     │  NLP Engine  │
│   (v1/api)    │◄────►│  (services/)     │◄───►│   (nlp/)     │
└───────┬───────┘      └────────┬─────────┘     └──────┬───────┘
        │                       │                       │
        │              ┌────────┴────────┐             │
        │              ▼                 ▼             │
        │      ┌──────────────┐  ┌──────────────┐     │
        │      │  News        │  │  Analysis    │     │
        │      │  Service     │  │  Service     │     │
        │      └──────┬───────┘  └──────┬───────┘     │
        │             │                 │             │
        └─────────────┼─────────────────┼─────────────┘
                      │                 │
        ┌─────────────┴─────────────────┴─────────────┐
        │                                             │
        ▼                                             ▼
┌────────────────┐                          ┌─────────────────┐
│  PostgreSQL    │                          │     Redis       │
│   (Primary)    │                          │   (Cache/RL)    │
│                │                          │                 │
│ - Articles     │                          │ - Rate Limits   │
│ - Entities     │                          │ - Cache Layer   │
│ - Trends       │                          │ - Pub/Sub       │
│ - Full-Text    │                          │ - Sessions      │
│   Search       │                          │                 │
└────────────────┘                          └─────────────────┘
```

---

## Component Architecture

### 1. API Layer (`app/api/v1/`)

**Responsibilities:**
- RESTful endpoint definitions
- Request/response validation
- HTTP error handling
- API versioning

**Key Components:**
- `endpoints/articles.py`: Article CRUD, search, advanced filtering
- `endpoints/analysis.py`: NLP analysis endpoints (sentiment, entities, topics)
- `endpoints/entities.py`: Entity management
- `endpoints/trends.py`: Trend detection and retrieval
- `endpoints/health.py`: Health checks and monitoring

**Technology:**
- FastAPI with async/await
- Pydantic for schema validation
- Dependency injection for service layer

### 2. Service Layer (`app/services/`)

**Responsibilities:**
- Business logic implementation
- Data aggregation and transformation
- Transaction management
- Cache orchestration

**Key Services:**

**NewsService** (`news_service.py`):
```python
class NewsService:
    async def create_article(data: ArticleCreate) -> Article
    async def get_articles(skip, limit) -> List[Article]
    async def search_articles(q, language) -> List[Article]
    async def advanced_search(filters) -> List[Article]
    async def update_article(id, data) -> Article
    async def delete_article(id) -> bool
```

**AnalysisService** (`analysis_service.py`):
```python
class AnalysisService:
    async def analyze_sentiment(text, language) -> SentimentResult
    async def extract_entities(text, language) -> List[Entity]
    async def extract_topics(text, language, num) -> List[Topic]
    async def analyze_graph(article_ids, type) -> GraphData
    async def batch_analysis(texts, types) -> List[AnalysisResult]
```

### 3. NLP Engine (`app/nlp/`)

**Responsibilities:**
- Natural language processing
- Persian/English text analysis
- Model loading and inference
- Entity recognition
- Sentiment classification

**Architecture:**
```
┌─────────────────────────────────────┐
│         NLP Coordinator             │
│  (Language Detection & Routing)     │
└──────────┬──────────────────────────┘
           │
    ┌──────┴───────┐
    ▼              ▼
┌─────────┐   ┌─────────┐
│  Hazm   │   │  spaCy  │
│ Persian │   │ English │
│ Engine  │   │ Engine  │
└────┬────┘   └────┬────┘
     │             │
     └──────┬──────┘
            ▼
    ┌──────────────┐
    │   Gensim     │
    │ Topic Model  │
    └──────────────┘
```

**Models:**
- **Hazm** (Persian): Tokenization, POS tagging, lemmatization, NER
- **spaCy** (English): en_core_web_md for NER, POS, dependencies
- **Gensim**: LDA for topic modeling, Word2Vec for embeddings

### 4. Data Layer

#### PostgreSQL Schema

```sql
-- Articles table with full-text search
CREATE TABLE news_articles (
    id SERIAL PRIMARY KEY,
    title VARCHAR(500) NOT NULL,
    content TEXT NOT NULL,
    url VARCHAR(2000) UNIQUE NOT NULL,
    source VARCHAR(200),
    category VARCHAR(100),
    published_date TIMESTAMP,
    language VARCHAR(10),
    tags TEXT[],
    sentiment_score FLOAT,
    search_vector tsvector,  -- Full-text search
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Full-text search index
CREATE INDEX idx_search_vector ON news_articles USING GIN(search_vector);
CREATE INDEX idx_published_date ON news_articles(published_date DESC);
CREATE INDEX idx_category ON news_articles(category);

-- Entities table
CREATE TABLE entities (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    entity_type VARCHAR(50) NOT NULL,
    frequency INT DEFAULT 1,
    first_seen TIMESTAMP DEFAULT NOW(),
    last_seen TIMESTAMP DEFAULT NOW()
);

-- Trends table
CREATE TABLE trends (
    id SERIAL PRIMARY KEY,
    topic VARCHAR(200) NOT NULL,
    score FLOAT NOT NULL,
    start_date TIMESTAMP,
    end_date TIMESTAMP,
    article_count INT DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE
);

-- Article-Entity relationships
CREATE TABLE article_entities (
    article_id INT REFERENCES news_articles(id) ON DELETE CASCADE,
    entity_id INT REFERENCES entities(id) ON DELETE CASCADE,
    confidence FLOAT,
    PRIMARY KEY (article_id, entity_id)
);
```

#### Redis Data Structures

```
# Rate limiting (per IP)
rate_limit:{ip}:minute -> counter (TTL: 60s)
rate_limit:{ip}:hour -> counter (TTL: 3600s)

# Cache layers
article:{id} -> JSON (TTL: 300s)
search:{hash} -> JSON array (TTL: 60s)
analysis:{article_id}:{type} -> JSON (TTL: 600s)

# Pub/Sub channels
events:articles -> new article notifications
events:analysis -> analysis completion
```

---

## Data Flow

### Article Creation Flow

```
Client Request
    │
    ▼
API Validation (Pydantic)
    │
    ▼
NewsService.create_article()
    │
    ├──► Check duplicate URL (PostgreSQL)
    │
    ├──► NLP Analysis (async)
    │    ├──► Sentiment analysis
    │    ├──► Entity extraction
    │    └──► Topic extraction
    │
    ├──► Save to PostgreSQL
    │    └──► Update search_vector
    │
    ├──► Cache article (Redis)
    │
    └──► Return response
```

### Search Flow (Full-Text)

```
Client Search Query
    │
    ▼
Check Redis cache (search:{hash})
    │
    ├──► Cache HIT ──► Return cached results
    │
    └──► Cache MISS
         │
         ▼
    PostgreSQL full-text search
    SELECT *, ts_rank(search_vector, query) as rank
    FROM news_articles
    WHERE search_vector @@ to_tsquery(query)
    ORDER BY rank DESC
         │
         ▼
    Cache results (Redis, TTL: 60s)
         │
         ▼
    Return results
```

### Analysis Flow (Batch)

```
Batch Analysis Request
    │
    ▼
AnalysisService.batch_analysis()
    │
    ├──► Group by language (Persian/English)
    │
    ├──► Persian texts ──► Hazm pipeline
    │                       ├──► Tokenize
    │                       ├──► POS tag
    │                       ├──► NER
    │                       └──► Sentiment
    │
    ├──► English texts ──► spaCy pipeline
    │                       ├──► Parse
    │                       ├──► NER
    │                       └──► Sentiment
    │
    ├──► Topic modeling (Gensim LDA)
    │
    ├──► Aggregate results
    │
    └──► Return analysis
```

---

## Scalability Considerations

### Horizontal Scaling

**Current State:**
- Stateless API layer (easy to scale)
- Shared PostgreSQL and Redis

**Future State (v2.0):**
```
┌──────────┐   ┌──────────┐   ┌──────────┐
│  API #1  │   │  API #2  │   │  API #3  │
└─────┬────┘   └─────┬────┘   └─────┬────┘
      │              │              │
      └──────────────┼──────────────┘
                     │
            ┌────────┴────────┐
            │  Load Balancer  │
            └────────┬────────┘
                     │
      ┌──────────────┼──────────────┐
      │              │              │
      ▼              ▼              ▼
┌──────────┐   ┌──────────┐   ┌──────────┐
│  PG #1   │   │  PG #2   │   │  PG #3   │
│ (Master) │──►│ (Read #1)│   │ (Read #2)│
└──────────┘   └──────────┘   └──────────┘

┌──────────┐   ┌──────────┐   ┌──────────┐
│ Redis #1 │   │ Redis #2 │   │ Redis #3 │
│ (Master) │──►│ (Replica)│   │ (Replica)│
└──────────┘   └──────────┘   └──────────┘
```

### Performance Optimization

**Database:**
- Connection pooling (SQLAlchemy async pool)
- Query optimization with indexes
- Materialized views for trends
- Partitioning by date (monthly)

**Caching Strategy:**
- L1: In-memory cache (per-instance)
- L2: Redis distributed cache
- Cache invalidation on updates
- TTL-based expiration

**NLP Processing:**
- Model preloading at startup
- Batch processing for efficiency
- GPU acceleration (optional)
- Async processing with queues

---

## Security Architecture

### Authentication & Authorization

**Current (v1.0 - Free Edition):**
- No authentication (open API)
- Rate limiting by IP

**Future (v2.0 - Pro Edition):**
```
┌──────────────────────────────────┐
│      API Key / JWT Token         │
└───────────┬──────────────────────┘
            │
            ▼
    ┌───────────────┐
    │  Auth Service │
    │   (OAuth2)    │
    └───────┬───────┘
            │
    ┌───────┴────────┐
    │                │
    ▼                ▼
┌────────┐      ┌────────┐
│  RBAC  │      │  Quota │
│ Roles  │      │ Limits │
└────────┘      └────────┘
```

### Security Layers

1. **Network Security:**
   - HTTPS/TLS for all traffic
   - CORS configuration
   - IP whitelisting (optional)

2. **Application Security:**
   - Input validation (Pydantic)
   - SQL injection prevention (SQLAlchemy ORM)
   - XSS protection (sanitization)
   - Rate limiting (DDoS protection)

3. **Data Security:**
   - Encrypted connections (PostgreSQL SSL)
   - Redis AUTH enabled
   - Environment variable secrets
   - No sensitive data logging

---

## Deployment Architecture

### Development Environment

```
Docker Compose:
  - FastAPI container (port 8000)
  - PostgreSQL container (port 5432)
  - Redis container (port 6379)
  - Alembic migrations
```

### Staging Environment (Kubernetes)

```yaml
# Namespace: aras-staging
- Deployment: api (replicas: 2)
- Service: api-service (LoadBalancer)
- StatefulSet: postgresql (replicas: 1)
- StatefulSet: redis (replicas: 1)
- ConfigMap: app-config
- Secret: db-credentials
- PVC: postgres-data (10Gi)
```

### Production Environment (Kubernetes)

```yaml
# Namespace: aras-production
- Deployment: api (replicas: 5, HPA enabled)
- Service: api-service (LoadBalancer)
- StatefulSet: postgresql (replicas: 3 with replication)
- StatefulSet: redis (replicas: 3 in cluster mode)
- Ingress: nginx-ingress (SSL termination)
- ConfigMap: app-config
- Secret: db-credentials, redis-auth, api-keys
- PVC: postgres-data (100Gi SSD)
- HPA: CPU 70%, min: 3, max: 10
```

---

## Monitoring & Observability

### Metrics Collection

```
Application Metrics:
  - Request rate, latency, error rate
  - Endpoint-specific performance
  - Cache hit/miss ratios
  - Database query performance

System Metrics:
  - CPU, memory, disk I/O
  - Network throughput
  - Container resource usage

Business Metrics:
  - Articles processed per hour
  - Analysis requests
  - Unique entities discovered
  - Trending topics count
```

### Logging Strategy

```python
# Structured logging
{
  "timestamp": "2025-11-13T10:00:00Z",
  "level": "INFO",
  "service": "api",
  "endpoint": "/api/v1/articles/",
  "method": "POST",
  "status": 201,
  "duration_ms": 234,
  "user_ip": "192.168.1.1",
  "trace_id": "abc123"
}
```

**Log Aggregation:**
- ELK Stack (Elasticsearch, Logstash, Kibana)
- CloudWatch Logs (AWS deployment)
- Loki + Grafana (K8s deployment)

### Alerting

**Critical Alerts:**
- API error rate > 5%
- Database connection failures
- Redis unavailable
- P95 latency > 2 seconds

**Warning Alerts:**
- Cache miss rate > 40%
- Disk usage > 80%
- Memory usage > 85%
- Rate limit hits > 100/min

---

## Technology Stack Summary

| Layer | Technology | Purpose |
|-------|-----------|---------|
| API Framework | FastAPI | Async REST API |
| Language | Python 3.12+ | Core development |
| Database | PostgreSQL 16 | Primary data store |
| Cache | Redis 7.x | Caching, rate limiting |
| ORM | SQLAlchemy 2.0 | Database abstraction |
| Migration | Alembic | Schema versioning |
| NLP (Persian) | Hazm | Persian text processing |
| NLP (English) | spaCy | English NER, POS |
| Topic Modeling | Gensim | LDA, Word2Vec |
| Testing | pytest | Unit/integration tests |
| Code Quality | Black, isort, Flake8 | Linting, formatting |
| Security | Bandit | Static analysis |
| Containerization | Docker | Application packaging |
| Orchestration | Kubernetes | Production deployment |
| CI/CD | GitHub Actions | Automation pipeline |
| Monitoring | Prometheus + Grafana | Metrics and dashboards |
| Logging | ELK Stack | Log aggregation |

---

## Version History

- **v1.0.0** (Target: 2026-01-31): Initial release with full-text search, NLP analysis, rate limiting
- **v0.1.0** (Current): Development phase, core features implementation

---

*Last Updated: 2025-11-13*
