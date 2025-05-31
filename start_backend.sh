#!/bin/bash

echo "🔄 Starting database initialization..."
echo "Current directory: $(pwd)"
echo "Python version: $(python --version)"

# check environment variables
echo "Checking environment variables..."
if [ -z "$DATABASE_URL" ]; then
    echo "Error: DATABASE_URL is not set"
    exit 1
fi

# run database initialization script
echo "Running database initialization script..."
python -m app.init_db

# check exit status of initialization script
if [ $? -ne 0 ]; then
    echo "Error: Database initialization failed"
    exit 1
fi

echo "✅ Database initialization completed successfully"

echo "🚀 Starting FastAPI server with uvicorn..."
uvicorn app.main:app --host 0.0.0.0 --port $PORT
