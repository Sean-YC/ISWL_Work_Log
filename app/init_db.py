from sqlalchemy import create_engine, text
import os
import sys
from dotenv import load_dotenv
import logging

# 设置日志
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

        logger.info("Connecting to database...")
        engine = create_engine(DATABASE_URL)
        
        # create users table (if not exists)
        with engine.begin() as conn:  # use begin() to handle transactions automatically
            # check if table exists
            logger.info("Checking if users table exists...")
            result = conn.execute(text("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_name = 'users'
                );
            """))
            table_exists = result.scalar()
            
            if not table_exists:
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
                logger.info("Users table created successfully!")
            else:
                logger.info("Users table already exists.")
                
                # check if username column exists
                logger.info("Checking if username column exists...")
                result = conn.execute(text("""
                    SELECT EXISTS (
                        SELECT FROM information_schema.columns 
                        WHERE table_name = 'users' AND column_name = 'username'
                    );
                """))
                column_exists = result.scalar()
                
                if not column_exists:
                    logger.info("Adding username column...")
                    conn.execute(text("""
                        ALTER TABLE users ADD COLUMN username VARCHAR UNIQUE;
                    """))
                    logger.info("Username column added successfully!")
                else:
                    logger.info("Username column already exists.")
            
            logger.info("Database initialization completed successfully!")
            
    except Exception as e:
        logger.error(f"Error during database initialization: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    init_db() 