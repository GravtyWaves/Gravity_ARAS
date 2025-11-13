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

### Search Articles

```http
GET /api/v1/articles/search/?query=keyword&language=en
```

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

### Graph Analysis

```http
POST /api/v1/analysis/graph
Content-Type: application/json
```

### Batch Analysis

```http
POST /api/v1/analysis/batch
Content-Type: application/json
```

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

- **Free Edition:** 100 requests per minute per IP
- **Headers:**
  - `X-RateLimit-Limit`: Maximum requests allowed
  - `X-RateLimit-Remaining`: Remaining requests
  - `X-RateLimit-Reset`: Time when limit resets

---

## Interactive Documentation

Visit these URLs for interactive API documentation:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc
