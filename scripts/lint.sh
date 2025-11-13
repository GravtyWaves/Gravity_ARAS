#!/bin/bash
# Code quality checks

set -e

echo "🔍 Running code quality checks..."

# Activate virtual environment if exists
if [ -d ".venv" ]; then
    source .venv/bin/activate
fi

echo "📝 Running Black formatter check..."
black --check app/ tests/

echo "📝 Running isort check..."
isort --check-only app/ tests/

echo "📝 Running mypy type checker..."
mypy app/

echo "📝 Running flake8 linter..."
flake8 app/ tests/ --max-line-length=88 --extend-ignore=E203

echo "✅ All code quality checks passed!"
