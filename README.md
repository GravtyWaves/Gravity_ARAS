# ARAS Microservice

[![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Advanced Reusable Analysis System (ARAS) - A comprehensive microservice for intelligent news analysis, entity extraction, sentiment analysis, and trend detection.

## 🚀 Features

- **Multi-language Support**: English and Persian (Farsi) text analysis
- **Advanced NLP**: Sentiment analysis, entity extraction, topic modeling
- **Graph Analysis**: Relationship extraction and network analysis
- **Real-time Processing**: Async operations with Celery for background tasks
- **Database Agnostic**: Support for PostgreSQL, MySQL, SQLite
- **Caching**: Redis integration for performance optimization
- **RESTful API**: Well-documented endpoints with OpenAPI/Swagger
- **Docker Ready**: Containerized deployment with Docker Compose
- **Monitoring**: Health checks and structured logging
- **Security**: JWT authentication and CORS support

## 🏗️ Architecture

```
ARAS Microservice
├── API Layer (FastAPI)
├── Service Layer (Business Logic)
├── Data Layer (SQLAlchemy ORM)
├── Cache Layer (Redis)
├── NLP Engine (spaCy, Hazm, Transformers)
├── Background Tasks (Celery)
└── Monitoring (Health Checks, Logging)
```

## 📋 Prerequisites

- Python 3.9+
- Docker & Docker Compose (for containerized deployment)
- PostgreSQL or Redis (optional, can use SQLite for development)

## 🛠️ Installation

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/aras-team/aras-microservice.git
   cd aras-microservice
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -e .
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Run database migrations**
   ```bash
   alembic upgrade head
   ```

6. **Start the application**
   ```bash
   uvicorn app.main:app --reload
   ```

### Docker Deployment

1. **Build and run with Docker Compose**
   ```bash
   docker-compose up --build
   ```

2. **Access the application**
   - API: http://localhost:8000
   - Documentation: http://localhost:8000/docs
   - Health Check: http://localhost:8000/health

## 📖 API Documentation

Once the application is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI Schema**: http://localhost:8000/openapi.json

### Key Endpoints

#### Health Check
```http
GET /health
```

#### Articles Management
```http
POST   /api/v1/articles/          # Create article
GET    /api/v1/articles/          # List articles
GET    /api/v1/articles/{id}      # Get article
PUT    /api/v1/articles/{id}      # Update article
DELETE /api/v1/articles/{id}      # Delete article
GET    /api/v1/articles/search/   # Search articles
```

#### Analysis Endpoints
```http
POST /api/v1/analysis/sentiment   # Sentiment analysis
POST /api/v1/analysis/entities    # Entity extraction
POST /api/v1/analysis/topics      # Topic modeling
POST /api/v1/analysis/graph       # Graph analysis
POST /api/v1/analysis/batch       # Batch analysis
```

#### Entities & Trends
```http
GET    /api/v1/entities/          # List entities
GET    /api/v1/entities/{id}      # Get entity
GET    /api/v1/trends/            # List trends
GET    /api/v1/trends/active/     # Active trends
```

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_health.py

# Run async tests
pytest -m asyncio
```

## 🔧 Configuration

The application uses environment variables for configuration. Copy `.env.example` to `.env` and modify as needed:

```env
# Database
DATABASE_URL=postgresql+asyncpg://user:password@localhost/aras_db

# Redis
REDIS_URL=redis://localhost:6379

# Security
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret

# NLP Models
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