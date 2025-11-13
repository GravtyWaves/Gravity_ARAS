#!/bin/bash
# Start development server

set -e

echo "🚀 Starting ARAS development server..."

# Activate virtual environment if exists
if [ -d ".venv" ]; then
    source .venv/bin/activate
fi

# Run database migrations
echo "🔄 Running migrations..."
alembic upgrade head

# Start Uvicorn server
echo "🌐 Starting FastAPI server..."
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
