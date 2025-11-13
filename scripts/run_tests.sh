#!/bin/bash
# Run tests with coverage

set -e

echo "🧪 Running ARAS tests..."

# Activate virtual environment if exists
if [ -d ".venv" ]; then
    source .venv/bin/activate
fi

# Run pytest with coverage
pytest tests/ -v \
    --cov=app \
    --cov-report=term-missing \
    --cov-report=html:htmlcov \
    --cov-fail-under=95

echo "✅ Tests completed!"
echo "📊 Coverage report: htmlcov/index.html"
