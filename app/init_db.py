from sqlalchemy import create_engine, text
import os
import sys
from dotenv import load_dotenv
import logging

# set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

def init_db():
    try:
        # Get DATABASE_URL from environment variable
        DATABASE_URL = os.getenv("DATABASE_URL")
        if not DATABASE_URL:
            logger.error("DATABASE_URL environment variable is not set")
            sys.exit(1)

        # print database connection information (hide password)
        masked_url = DATABASE_URL.replace(DATABASE_URL.split('@')[0], '***')
        logger.info(f"Connecting to database: {masked_url}")

        engine = create_engine(DATABASE_URL)
        
        with engine.begin() as conn:
            # Drop existing tables if they exist
            logger.info("Dropping existing tables...")
            conn.execute(text("""
                DROP TABLE IF EXISTS logs CASCADE;
                DROP TABLE IF EXISTS users CASCADE;
            """))
            
            # Create users table
            logger.info("Creating users table...")
            conn.execute(text("""
                CREATE TABLE users (
                    id SERIAL PRIMARY KEY,
                    email VARCHAR UNIQUE NOT NULL,
                    username VARCHAR UNIQUE,
                    hashed_password VARCHAR NOT NULL,
                    role VARCHAR NOT NULL
                );
            """))
            
            # Create logs table
            logger.info("Creating logs table...")
            conn.execute(text("""
                CREATE TABLE logs (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER NOT NULL REFERENCES users(id),
                    week_number INTEGER NOT NULL,
                    day VARCHAR NOT NULL,
                    date DATE,
                    working_hours FLOAT,
                    task_description VARCHAR,
                    status VARCHAR DEFAULT 'pending',
                    reviewer_id INTEGER REFERENCES users(id)
                );
            """))
            
            # print current table structure
            logger.info("Checking current table structure...")
            result = conn.execute(text("""
                SELECT table_name, column_name, data_type, is_nullable 
                FROM information_schema.columns 
                WHERE table_name IN ('users', 'logs')
                ORDER BY table_name, ordinal_position;
            """))
            columns = [(row[0], row[1], row[2], row[3]) for row in result]
            logger.info("Current database structure:")
            current_table = None
            for table, col, dtype, nullable in columns:
                if table != current_table:
                    current_table = table
                    logger.info(f"\n{table} table:")
                logger.info(f"  - {col}: {dtype} (nullable: {nullable})")
            
            logger.info("Database initialization completed successfully!")
            
    except Exception as e:
        logger.error(f"Error during database initialization: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    init_db() 