#!/bin/sh

set -e

echo "Running migrations..."
alembic upgrade head

echo "Starting FastAPI..."
exec fastapi run --host 0.0.0.0 --port 8000