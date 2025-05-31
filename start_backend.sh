#!/bin/bash

echo "🔄 Starting database initialization..."
echo "Current directory: $(pwd)"
echo "Python version: $(python --version)"
echo "Python path: $(which python)"
echo "Current user: $(whoami)"

# check environment variables
echo "Checking environment variables..."
if [ -z "$DATABASE_URL" ]; then
    echo "Error: DATABASE_URL is not set"
    exit 1
fi

# check if init_db.py exists
echo "Checking if init_db.py exists..."
if [ ! -f "app/init_db.py" ]; then
    echo "Error: app/init_db.py not found"
    ls -la app/
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

# verify database structure
echo "Verifying database structure..."
python -c "
import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()
engine = create_engine(os.getenv('DATABASE_URL'))
with engine.connect() as conn:
    result = conn.execute(text('SELECT column_name FROM information_schema.columns WHERE table_name = \'users\';'))
    columns = [row[0] for row in result]
    print('Current columns in users table:', columns)
"

echo "🚀 Starting FastAPI server with uvicorn..."
uvicorn app.main:app --host 0.0.0.0 --port $PORT
