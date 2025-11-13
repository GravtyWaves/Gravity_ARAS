#!/bin/bash
# Initialize database and run migrations

set -e

echo "🗄️  Initializing ARAS database..."

# Wait for PostgreSQL to be ready
echo "⏳ Waiting for PostgreSQL..."
while ! pg_isready -h ${DB_HOST:-localhost} -p ${DB_PORT:-5432} -U ${DB_USER:-aras_user}; do
  sleep 1
done

echo "✅ PostgreSQL is ready!"

# Run Alembic migrations
echo "🔄 Running database migrations..."
alembic upgrade head

echo "✅ Database initialized successfully!"
