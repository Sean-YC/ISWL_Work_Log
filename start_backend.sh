#!/bin/bash

echo "🔄 Initializing database..."
python -m app.init_db

echo "🚀 Starting FastAPI server with uvicorn..."
uvicorn app.main:app --host 0.0.0.0 --port $PORT
