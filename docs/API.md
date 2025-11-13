# ARAS Microservice - API Documentation

## Overview

ARAS (Advanced Reusable Analysis System) provides a comprehensive RESTful API for news analysis, entity extraction, sentiment analysis, and trend detection.

**Base URL:** `http://localhost:8000`  
**API Version:** v1  
**Authentication:** Bearer Token (Optional for free edition)

---

## Health Check

### Check System Health

```http
GET /health
```

**Response:**
```json
{
  "success": true,
  "data": {
    "status": "healthy",
    "timestamp": "2025-11-13T10:00:00Z",
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

---

## Articles

### Create Article

```http
POST /api/v1/articles/
Content-Type: application/json
```

**Request Body:**
```json
{
  "title": "Article Title",
  "content": "Full article content...",
  "url": "https://example.com/article",
  "source": "News Source",
  "published_date": "2025-11-13T10:00:00Z",
  "language": "en",
  "tags": ["politics", "economy"]
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "article": {
      "id": 1,
      "title": "Article Title",
      "content": "Full article content...",
      "url": "https://example.com/article",
      "source": "News Source",
      "published_date": "2025-11-13T10:00:00Z",
      "language": "en",
      "tags": ["politics", "economy"],
      "created_at": "2025-11-13T10:00:00Z"
    }
  },
  "message": "Article created successfully"
}
```

### List Articles

```http
GET /api/v1/articles/?skip=0&limit=10
```

**Query Parameters:**
- `skip` (integer, optional): Number of records to skip (default: 0)
- `limit` (integer, optional): Maximum records to return (default: 10)

### Get Article by ID

```http
GET /api/v1/articles/{id}
```

### Update Article

```http
PUT /api/v1/articles/{id}
Content-Type: application/json
```

### Delete Article

```http
DELETE /api/v1/articles/{id}
```

### Search Articles (Basic Full-Text)

```http
GET /api/v1/articles/search/?q=keyword&language=en&skip=0&limit=10
```

**Query Parameters:**
- `q` (string, required): Search query for full-text search
- `language` (string, optional): Filter by language (en, fa)
- `skip` (integer, optional): Number of records to skip (default: 0)
- `limit` (integer, optional): Maximum records to return (default: 10, max: 100)

**Response:**
```json
{
  "success": true,
  "data": {
    "articles": [
      {
        "id": 1,
        "title": "Matching Article Title",
        "content": "Article content with keyword...",
        "url": "https://example.com/article",
        "source": "News Source",
        "published_date": "2025-11-13T10:00:00Z",
        "language": "en",
        "tags": ["politics"],
        "relevance_score": 0.456,
        "created_at": "2025-11-13T10:00:00Z"
      }
    ],
    "total": 42,
    "skip": 0,
    "limit": 10
  }
}
```

**Note:** Uses PostgreSQL full-text search with `ts_rank` for relevance scoring.

### Advanced Search

```http
POST /api/v1/articles/search/advanced
Content-Type: application/json
```

**Request Body:**
```json
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

**Parameters:**
- `q` (string, optional): Full-text search query
- `category` (string, optional): Filter by article category
- `source` (string, optional): Filter by news source
- `language` (string, optional): Filter by language (en, fa)
- `tags` (array[string], optional): Filter by tags (AND condition)
- `sentiment_min` (float, optional): Minimum sentiment score (-1.0 to 1.0)
- `sentiment_max` (float, optional): Maximum sentiment score (-1.0 to 1.0)
- `start_date` (datetime, optional): Filter articles after this date
- `end_date` (datetime, optional): Filter articles before this date
- `skip` (integer, optional): Pagination offset (default: 0)
- `limit` (integer, optional): Results per page (default: 10, max: 100)

**Response:**
```json
{
  "success": true,
  "data": {
    "articles": [/* same structure as basic search */],
    "total": 15,
    "skip": 0,
    "limit": 20,
    "filters_applied": {
      "q": "climate change",
      "category": "environment",
      "source": "BBC News",
      "language": "en",
      "tags": ["climate", "policy"],
      "sentiment_range": [0.3, 0.8],
      "date_range": ["2025-01-01", "2025-12-31"]
    }
  }
}
```

**Rate Limit:** 30 requests per minute per IP (moderate tier)

---

## Analysis

### Sentiment Analysis

```http
POST /api/v1/analysis/sentiment
Content-Type: application/json
```

**Request Body:**
```json
{
  "text": "This is a great article!",
  "language": "en"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "analysis": {
      "sentiment": "positive",
      "confidence": 0.85,
      "scores": {
        "positive": 0.85,
        "neutral": 0.10,
        "negative": 0.05
      }
    }
  }
}
```

### Entity Extraction

```http
POST /api/v1/analysis/entities
Content-Type: application/json
```

**Request Body:**
```json
{
  "text": "Barack Obama visited Microsoft headquarters in Seattle.",
  "language": "en"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "entities": [
      {
        "text": "Barack Obama",
        "type": "PERSON",
        "confidence": 0.95
      },
      {
        "text": "Microsoft",
        "type": "ORGANIZATION",
        "confidence": 0.92
      },
      {
        "text": "Seattle",
        "type": "LOCATION",
        "confidence": 0.88
      }
    ]
  }
}
```

### Topic Extraction

```http
POST /api/v1/analysis/topics
Content-Type: application/json
```

**Request Body:**
```json
{
  "text": "Long article about artificial intelligence, machine learning, and neural networks...",
  "language": "en",
  "num_topics": 3
}
```

**Parameters:**
- `text` (string, required): Text to extract topics from
- `language` (string, required): Language code (en, fa)
- `num_topics` (integer, optional): Number of topics to extract (default: 5, max: 10)

**Response:**
```json
{
  "success": true,
  "data": {
    "topics": [
      {
        "topic": "artificial intelligence",
        "confidence": 0.92,
        "keywords": ["AI", "machine learning", "neural networks"],
        "relevance_score": 0.88
      },
      {
        "topic": "technology",
        "confidence": 0.85,
        "keywords": ["innovation", "computing", "algorithms"],
        "relevance_score": 0.76
      },
      {
        "topic": "data science",
        "confidence": 0.73,
        "keywords": ["data", "analysis", "models"],
        "relevance_score": 0.65
      }
    ],
    "language": "en",
    "processing_time_ms": 156
  }
}
```

### Graph Analysis

```http
POST /api/v1/analysis/graph
Content-Type: application/json
```

**Request Body:**
```json
{
  "article_ids": [1, 2, 3, 4, 5],
  "analysis_type": "entity_network",
  "min_edge_weight": 0.3
}
```

**Parameters:**
- `article_ids` (array[int], required): IDs of articles to analyze
- `analysis_type` (string, required): Type of graph analysis
  - `entity_network`: Entity co-occurrence network
  - `topic_network`: Topic relationship network
  - `source_network`: News source citation network
- `min_edge_weight` (float, optional): Minimum edge weight threshold (0.0-1.0, default: 0.2)

**Response:**
```json
{
  "success": true,
  "data": {
    "graph": {
      "nodes": [
        {"id": "entity_1", "label": "Tesla", "type": "ORGANIZATION", "centrality": 0.85},
        {"id": "entity_2", "label": "Elon Musk", "type": "PERSON", "centrality": 0.92},
        {"id": "entity_3", "label": "SpaceX", "type": "ORGANIZATION", "centrality": 0.78}
      ],
      "edges": [
        {"source": "entity_1", "target": "entity_2", "weight": 0.95, "co_occurrences": 12},
        {"source": "entity_2", "target": "entity_3", "weight": 0.87, "co_occurrences": 8},
        {"source": "entity_1", "target": "entity_3", "weight": 0.65, "co_occurrences": 5}
      ],
      "metrics": {
        "total_nodes": 3,
        "total_edges": 3,
        "avg_degree": 2.0,
        "density": 0.67,
        "clustering_coefficient": 0.83
      }
    },
    "analysis_type": "entity_network",
    "articles_analyzed": 5,
    "processing_time_ms": 423
  }
}
```

**Rate Limit:** 30 requests per minute (moderate tier)

---

### Batch Analysis

```http
POST /api/v1/analysis/batch
Content-Type: application/json
```

**Request Body:**
```json
{
  "texts": [
    {
      "id": "article_1",
      "text": "First article content...",
      "language": "en"
    },
    {
      "id": "article_2", 
      "text": "محتوای مقاله دوم به فارسی...",
      "language": "fa"
    }
  ],
  "analysis_types": ["sentiment", "entities", "topics"]
}
```

**Parameters:**
- `texts` (array, required): List of text objects to analyze
  - `id` (string, required): Unique identifier for text
  - `text` (string, required): Text content to analyze
  - `language` (string, required): Language code (en, fa)
- `analysis_types` (array, required): Types of analysis to perform
  - Allowed values: "sentiment", "entities", "topics", "keywords"

**Response:**
```json
{
  "success": true,
  "data": {
    "results": [
      {
        "id": "article_1",
        "sentiment": {
          "sentiment": "positive",
          "confidence": 0.82,
          "scores": {
            "positive": 0.82,
            "neutral": 0.12,
            "negative": 0.06
          }
        },
        "entities": [
          {"text": "Tesla", "type": "ORGANIZATION", "confidence": 0.91},
          {"text": "Elon Musk", "type": "PERSON", "confidence": 0.94}
        ],
        "topics": [
          {"topic": "technology", "confidence": 0.88},
          {"topic": "business", "confidence": 0.76}
        ]
      },
      {
        "id": "article_2",
        "sentiment": {
          "sentiment": "neutral",
          "confidence": 0.65,
          "scores": {
            "positive": 0.40,
            "neutral": 0.45,
            "negative": 0.15
          }
        },
        "entities": [/* Persian entities */],
        "topics": [/* Persian topics */]
      }
    ],
    "total_processed": 2,
    "processing_time_ms": 342
  }
}
```

**Rate Limit:** 10 requests per minute (strict tier)  
**Max batch size:** 50 texts per request

---

## Entities

### List Entities

```http
GET /api/v1/entities/?skip=0&limit=10
```

### Get Entity by ID

```http
GET /api/v1/entities/{id}
```

### Search Entities

```http
GET /api/v1/entities/search/?query=name&type=PERSON
```

---

## Trends

### List Trends

```http
GET /api/v1/trends/?skip=0&limit=10
```

### Get Active Trends

```http
GET /api/v1/trends/active/
```

### Get Trend by ID

```http
GET /api/v1/trends/{id}
```

---

## Error Responses

All error responses follow this format:

```json
{
  "success": false,
  "message": "Error description",
  "error_code": "ERROR_CODE",
  "timestamp": "2025-11-13T10:00:00Z"
}
```

**Common Error Codes:**
- `400` - Bad Request
- `404` - Not Found
- `500` - Internal Server Error

---

## Rate Limiting

ARAS implements multi-tier rate limiting based on endpoint sensitivity:

### Rate Limit Tiers

**Strict Tier** (Authentication, sensitive operations):
- 10 requests per minute
- 200 requests per hour
- Endpoints: `/api/v1/analysis/batch`, authentication endpoints

**Moderate Tier** (Advanced features):
- 30 requests per minute
- 500 requests per hour
- Endpoints: `/api/v1/articles/search/advanced`, `/api/v1/analysis/graph`

**Relaxed Tier** (Standard operations):
- 100 requests per minute
- 1000 requests per hour
- Endpoints: All other API endpoints

### Response Headers

All API responses include rate limit information:

```http
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1699876543
X-RateLimit-Window: 60
```

**Headers:**
- `X-RateLimit-Limit`: Maximum requests allowed in current window
- `X-RateLimit-Remaining`: Remaining requests in current window
- `X-RateLimit-Reset`: Unix timestamp when limit resets
- `X-RateLimit-Window`: Window duration in seconds (60 or 3600)

### Rate Limit Exceeded

When rate limit is exceeded, API returns:

```json
{
  "success": false,
  "message": "Rate limit exceeded. Try again in 45 seconds.",
  "error_code": "RATE_LIMIT_EXCEEDED",
  "retry_after": 45,
  "timestamp": "2025-11-13T10:00:00Z"
}
```

**HTTP Status:** `429 Too Many Requests`

### Implementation Details

- Rate limiting uses Redis for distributed counting
- Limits are per IP address
- Graceful degradation: if Redis unavailable, limits not enforced
- Resets occur at fixed intervals (not sliding windows)

---

## Interactive Documentation

Visit these URLs for interactive API documentation:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc
