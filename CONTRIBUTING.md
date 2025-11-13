# Contributing to ARAS Microservice

Thank you for considering contributing to ARAS! This document provides guidelines and best practices for contributing to the project.

## Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [Getting Started](#getting-started)
3. [Development Workflow](#development-workflow)
4. [Coding Standards](#coding-standards)
5. [Testing Guidelines](#testing-guidelines)
6. [Commit Message Guidelines](#commit-message-guidelines)
7. [Pull Request Process](#pull-request-process)
8. [Code Review Process](#code-review-process)

---

## Code of Conduct

This project adheres to a code of professionalism and respect:

- Be respectful and inclusive
- Focus on constructive feedback
- Prioritize project goals and quality
- Communicate clearly and professionally
- Follow all technical standards

---

## Getting Started

### Prerequisites

- Python 3.9+
- PostgreSQL 15+
- Redis 7+
- Docker and Docker Compose
- Git

### Setup Development Environment

```bash
# Clone repository
git clone https://github.com/your-org/aras-microservice.git
cd aras-microservice

# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -e .

# Setup environment
cp .env.example .env

# Start infrastructure
docker-compose up -d postgres redis

# Run migrations
alembic upgrade head

# Run tests
pytest
```

---

## Development Workflow

### 1. Create Feature Branch

```bash
git checkout -b feature/your-feature-name
```

**Branch naming convention:**
- `feature/description` - New features
- `fix/description` - Bug fixes
- `refactor/description` - Code refactoring
- `docs/description` - Documentation updates
- `test/description` - Test additions/updates

### 2. Make Changes

- Write clean, documented code
- Follow coding standards
- Add tests for new functionality
- Update documentation

### 3. Run Quality Checks

```bash
# Format code
black app/ tests/
isort app/ tests/

# Type checking
mypy app/

# Linting
flake8 app/ tests/

# Run tests
pytest tests/ -v --cov=app --cov-fail-under=95
```

### 4. Commit Changes

```bash
git add .
git commit -m "feat(module): add new feature"
```

### 5. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

---

## Coding Standards

### Python Style Guide

Follow **PEP 8** with these specifics:

- **Line length:** 88 characters (Black default)
- **Indentation:** 4 spaces
- **String quotes:** Double quotes for strings, single for dict keys
- **Import order:** stdlib, third-party, local (managed by isort)

### Type Hints

**Required for all functions:**

```python
from typing import Optional, List

def process_article(
    article_id: int,
    content: str,
    language: str = "en"
) -> Optional[dict]:
    """Process article and return analysis results."""
    pass
```

### Docstrings

**Use Google style docstrings:**

```python
def analyze_sentiment(text: str, language: str = "en") -> dict:
    """Analyze sentiment of given text.
    
    Args:
        text: Input text to analyze
        language: Language code (en, fa)
    
    Returns:
        Dictionary containing sentiment score and label
        
    Raises:
        ValueError: If language not supported
    """
    pass
```

### Error Handling

**Comprehensive error handling:**

```python
try:
    result = await process_data(data)
except ValidationError as e:
    logger.error(f"Validation error: {e}")
    raise HTTPException(status_code=400, detail=str(e))
except Exception as e:
    logger.exception("Unexpected error")
    raise HTTPException(status_code=500, detail="Internal server error")
```

---

## Testing Guidelines

### Test Coverage

- **Minimum:** 95% code coverage
- **Focus areas:** Core logic, API endpoints, database operations
- **Test types:** Unit, integration, end-to-end

### Test Structure

```python
import pytest
from httpx import AsyncClient

class TestArticlesAPI:
    """Test cases for articles API endpoints."""
    
    @pytest.mark.asyncio
    async def test_create_article_success(self, client: AsyncClient):
        """Test successful article creation."""
        response = await client.post("/api/v1/articles/", json={...})
        assert response.status_code == 201
        assert "article" in response.json()["data"]
    
    @pytest.mark.asyncio
    async def test_create_article_invalid_data(self, client: AsyncClient):
        """Test article creation with invalid data."""
        response = await client.post("/api/v1/articles/", json={})
        assert response.status_code == 400
```

### Running Tests

```bash
# All tests
pytest

# Specific test file
pytest tests/test_articles.py

# With coverage
pytest --cov=app --cov-report=html

# Verbose output
pytest -v

# Stop on first failure
pytest -x
```

---

## Commit Message Guidelines

### Format

Follow **Conventional Commits** specification:

```
<type>(<scope>): <subject>

[optional body]

[optional footer]
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `refactor`: Code refactoring
- `docs`: Documentation changes
- `test`: Test additions/updates
- `chore`: Maintenance tasks
- `style`: Code formatting
- `perf`: Performance improvements

### Examples

**Good commits:**

```bash
feat(api): add sentiment analysis endpoint

Implemented sentiment analysis endpoint using spaCy for English
and Hazm for Persian text analysis.

Closes #42

fix(database): resolve connection pool exhaustion

Connection pool was not releasing connections properly in error paths.
Added proper context managers and timeout configuration.

Performance improved from 500ms to 50ms per query.

docs(readme): update installation instructions

Added prerequisites section and troubleshooting guide.
```

**Bad commits:**

```bash
# Too vague
fix: fixed stuff

# Non-English
feat: اضافه کردن ویژگی جدید

# No description
update
```

---

## Pull Request Process

### Before Creating PR

1. ✅ All tests pass
2. ✅ Code coverage ≥ 95%
3. ✅ Code formatted (Black, isort)
4. ✅ Type checking passes (mypy)
5. ✅ Linting passes (flake8)
6. ✅ Documentation updated
7. ✅ Changelog updated (if applicable)

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
Describe testing performed

## Checklist
- [ ] Tests pass
- [ ] Coverage ≥ 95%
- [ ] Code formatted
- [ ] Documentation updated
- [ ] Changelog updated
```

### PR Title

Use conventional commit format:

```
feat(api): add batch analysis endpoint
fix(nlp): resolve Persian tokenization issue
docs(api): update entity extraction examples
```

---

## Code Review Process

### Reviewer Checklist

- [ ] Code follows style guidelines
- [ ] Changes are well-documented
- [ ] Tests are comprehensive
- [ ] No security vulnerabilities
- [ ] Performance impact considered
- [ ] Error handling is adequate
- [ ] API changes are backward compatible

### Review Comments

**Be constructive:**

✅ **Good:**
```
Consider using a set instead of list here for O(1) lookup performance.
```

❌ **Bad:**
```
This code is terrible.
```

### Approval Process

- **Small changes:** 1 approval required
- **Major changes:** 2 approvals required
- **Breaking changes:** All team leads approval

---

## Questions or Issues?

- **Technical Questions:** Open an issue with `question` label
- **Bug Reports:** Open an issue with `bug` label
- **Feature Requests:** Open an issue with `enhancement` label
- **Security Issues:** Email security@aras.ai (do NOT create public issue)

---

Thank you for contributing to ARAS! 🎉
