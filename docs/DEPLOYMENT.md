# ARAS Microservice - Deployment Guide

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Local Development Setup](#local-development-setup)
3. [Docker Deployment](#docker-deployment)
4. [Production Deployment](#production-deployment)
5. [Environment Configuration](#environment-configuration)
6. [Database Setup](#database-setup)
7. [Monitoring & Logging](#monitoring--logging)
8. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required Software

- **Python:** 3.9 or higher
- **PostgreSQL:** 15 or higher
- **Redis:** 7 or higher
- **Docker:** 20.10 or higher (for containerized deployment)
- **Docker Compose:** 2.0 or higher

### System Requirements

**Minimum (Development):**
- 2 CPU cores
- 4 GB RAM
- 20 GB storage

**Recommended (Production):**
- 4 CPU cores
- 8 GB RAM
- 50 GB SSD storage

---

## Local Development Setup

### 1. Clone Repository

```bash
git clone https://github.com/your-org/aras-microservice.git
cd aras-microservice
```

### 2. Create Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -e .
```

### 4. Configure Environment

```bash
cp .env.example .env
# Edit .env with your configuration
```

### 5. Initialize Database

```bash
# Start PostgreSQL and Redis
docker-compose up -d postgres redis

# Run migrations
alembic upgrade head
```

### 6. Start Development Server

```bash
./scripts/start_dev.sh
# Or manually:
# uvicorn app.main:app --reload
```

### 7. Access Application

- **API:** http://localhost:8000
- **Swagger Docs:** http://localhost:8000/docs
- **Health Check:** http://localhost:8000/health

---

## Docker Deployment

### Development Environment

```bash
# Build and start all services
docker-compose up --build

# Run in background
docker-compose up -d

# View logs
docker-compose logs -f aras-app

# Stop services
docker-compose down
```

### Services

- **aras-app:** FastAPI application (port 8000)
- **postgres:** PostgreSQL database (port 5432)
- **redis:** Redis cache (port 6379)
- **pgadmin:** Database management UI (port 5050)

---

## Production Deployment

### Option 1: VPS Deployment

#### 1. Prepare Server

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

#### 2. Clone and Configure

```bash
git clone https://github.com/your-org/aras-microservice.git
cd aras-microservice

# Configure environment
cp .env.example .env
nano .env  # Edit configuration
```

#### 3. Deploy Application

```bash
# Build and start
docker-compose up -d

# View logs
docker-compose logs -f
```

#### 4. Setup Nginx Reverse Proxy

```bash
sudo apt install nginx -y

# Create Nginx configuration
sudo nano /etc/nginx/sites-available/aras
```

**Nginx Configuration:**

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/aras /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### 5. Setup SSL (Let's Encrypt)

```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d your-domain.com
```

### Option 2: Kubernetes Deployment

```bash
# Apply Kubernetes manifests
kubectl apply -f k8s/

# Check deployment status
kubectl get pods -n aras
kubectl get services -n aras
```

---

## Environment Configuration

### Required Variables

```bash
# Database
DATABASE_URL=postgresql+asyncpg://user:password@localhost/aras_db

# Redis
REDIS_URL=redis://localhost:6379

# Security
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-here

# Application
DEBUG=False
API_V1_STR=/api/v1
PROJECT_NAME=ARAS

# CORS
ALLOWED_ORIGINS=https://your-domain.com
```

### Optional Variables

```bash
# NLP Models
SPACY_MODEL_EN=en_core_web_sm
SPACY_MODEL_FA=fa

# Crawler
CRAWLER_DELAY=5
CRAWLER_USER_AGENT=ARAS/1.0

# Celery
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
```

---

## Database Setup

### Manual Setup

```bash
# Create database
sudo -u postgres psql
CREATE DATABASE aras_db;
CREATE USER aras_user WITH PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE aras_db TO aras_user;
\q

# Run migrations
alembic upgrade head
```

### Backup Database

```bash
# Backup
pg_dump -U aras_user aras_db > backup.sql

# Restore
psql -U aras_user aras_db < backup.sql
```

---

## Monitoring & Logging

### Application Logs

```bash
# Docker logs
docker-compose logs -f aras-app

# Application logs (if running locally)
tail -f logs/aras.log
```

### Health Checks

```bash
# Check health endpoint
curl http://localhost:8000/health

# Expected response
{
  "success": true,
  "data": {
    "status": "healthy",
    "database": {"status": "connected"},
    "redis": {"status": "connected"}
  }
}
```

### Database Monitoring

```bash
# Connect to PostgreSQL
docker-compose exec postgres psql -U aras_user -d aras_db

# Check connections
SELECT * FROM pg_stat_activity;

# Database size
SELECT pg_size_pretty(pg_database_size('aras_db'));
```

---

## Troubleshooting

### Common Issues

#### 1. Database Connection Failed

```bash
# Check PostgreSQL is running
docker-compose ps postgres

# Check logs
docker-compose logs postgres

# Restart database
docker-compose restart postgres
```

#### 2. Redis Connection Failed

```bash
# Check Redis is running
docker-compose ps redis

# Test connection
redis-cli -h localhost -p 6379 ping
```

#### 3. Port Already in Use

```bash
# Find process using port 8000
sudo lsof -i :8000

# Kill process
kill -9 <PID>
```

#### 4. Migration Errors

```bash
# Reset database (WARNING: Data loss)
docker-compose down -v
docker-compose up -d postgres redis
alembic upgrade head
```

#### 5. Permission Denied

```bash
# Fix script permissions
chmod +x scripts/*.sh

# Fix Docker permissions
sudo usermod -aG docker $USER
newgrp docker
```

---

## Maintenance

### Update Application

```bash
# Pull latest code
git pull origin main

# Rebuild and restart
docker-compose down
docker-compose up --build -d

# Run migrations
docker-compose exec aras-app alembic upgrade head
```

### Database Maintenance

```bash
# Vacuum database
docker-compose exec postgres psql -U aras_user -d aras_db -c "VACUUM ANALYZE;"

# Reindex
docker-compose exec postgres psql -U aras_user -d aras_db -c "REINDEX DATABASE aras_db;"
```

---

## Security Best Practices

1. **Never commit `.env` files**
2. **Use strong passwords** for database
3. **Enable firewall** on production servers
4. **Regular backups** of database
5. **Keep dependencies updated**
6. **Use HTTPS** in production
7. **Implement rate limiting**
8. **Monitor logs** for suspicious activity

---

For additional support, see [README.md](../README.md) or contact the development team.
