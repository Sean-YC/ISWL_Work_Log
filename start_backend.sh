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

# run database initialization script with print statements
echo "Running database initialization script..."
PYTHONPATH=. python -c "
import sys
from app.init_db import init_db

print('Starting database initialization...')
try:
    init_db()
    print('Database initialization completed successfully!')
except Exception as e:
    print(f'Error during database initialization: {str(e)}', file=sys.stderr)
    sys.exit(1)
"

# check exit status of initialization script
if [ $? -ne 0 ]; then
    echo "Error: Database initialization failed"
    exit 1
fi

echo "✅ Database initialization completed successfully"

# verify database structure
echo "Verifying database structure..."
PYTHONPATH=. python -c "
import os
import sys
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()
engine = create_engine(os.getenv('DATABASE_URL'))

try:
    with engine.connect() as conn:
        # Check users table
        print('\nChecking users table...')
        result = conn.execute(text('SELECT column_name FROM information_schema.columns WHERE table_name = \'users\';'))
        columns = [row[0] for row in result]
        print('Current columns in users table:', columns)
        
        # Check if username column exists
        result = conn.execute(text('SELECT EXISTS (SELECT FROM information_schema.columns WHERE table_name = \'users\' AND column_name = \'username\');'))
        username_exists = result.scalar()
        print('Username column exists:', username_exists)
        
        if not username_exists:
            print('\nAttempting to add username column...')
            try:
                conn.execute(text('ALTER TABLE users ADD COLUMN username VARCHAR UNIQUE;'))
                print('Successfully added username column with UNIQUE constraint')
            except Exception as e:
                print('Failed to add username column with UNIQUE constraint:', str(e))
                try:
                    conn.execute(text('ALTER TABLE users ADD COLUMN username VARCHAR;'))
                    print('Successfully added username column without UNIQUE constraint')
                except Exception as e2:
                    print('Failed to add username column:', str(e2))
                    sys.exit(1)
except Exception as e:
    print('Error verifying database structure:', str(e), file=sys.stderr)
    sys.exit(1)
"

echo "🚀 Starting FastAPI server with uvicorn..."
uvicorn app.main:app --host 0.0.0.0 --port $PORT --log-level debug
