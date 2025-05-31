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
                
                # Directly try to add the username column
                logger.info("Attempting to add username column...")
                try:
                    # First, check if the column exists
                    result = conn.execute(text("""
                        SELECT column_name 
                        FROM information_schema.columns 
                        WHERE table_name = 'users' 
                        AND column_name = 'username';
                    """))
                    if not result.fetchone():
                        # Column doesn't exist, add it
                        conn.execute(text("""
                            ALTER TABLE users 
                            ADD COLUMN username VARCHAR UNIQUE;
                        """))
                        logger.info("Username column added successfully!")
                    else:
                        logger.info("Username column already exists.")
                except Exception as e:
                    logger.error(f"Error adding username column: {str(e)}")
                    # Try alternative approach
                    try:
                        logger.info("Trying alternative approach to add username column...")
                        conn.execute(text("""
                            ALTER TABLE users 
                            ADD COLUMN IF NOT EXISTS username VARCHAR UNIQUE;
                        """))
                        logger.info("Username column added using alternative approach!")
                    except Exception as e2:
                        logger.error(f"Alternative approach also failed: {str(e2)}")
                        raise
            
            # print current table structure
            logger.info("Checking current table structure...")
            result = conn.execute(text("""
                SELECT column_name, data_type, is_nullable 
                FROM information_schema.columns 
                WHERE table_name = 'users' 
                ORDER BY ordinal_position;
            """))
            columns = [(row[0], row[1], row[2]) for row in result]
            logger.info("Current users table structure:")
            for col in columns:
                logger.info(f"  - {col[0]}: {col[1]} (nullable: {col[2]})")
            
            logger.info("Database initialization completed successfully!")
            
    except Exception as e:
        logger.error(f"Error during database initialization: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    init_db() 