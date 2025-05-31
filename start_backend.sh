#!/bin/bash

echo "🔄 Running database migrations..."
alembic upgrade head

echo "🚀 Starting FastAPI server with uvicorn..."
uvicorn app.main:app --host 0.0.0.0 --port $PORT
