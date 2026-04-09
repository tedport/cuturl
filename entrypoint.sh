#!/bin/sh

set -e

echo "Running migrations..."
alembic upgrade head

echo "Starting FastAPI..."
exec fastapi run --port 8000