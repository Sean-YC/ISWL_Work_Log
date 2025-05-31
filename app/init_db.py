from sqlalchemy import create_engine, text
import os
import sys
from dotenv import load_dotenv
import logging
import traceback
from sqlalchemy.exc import SQLAlchemyError

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

        engine = create_engine(DATABASE_URL, echo=True)  # Enable SQL logging
        
        with engine.begin() as conn:
            try:
                # Check if users table exists
                logger.info("Checking if users table exists...")
                result = conn.execute(text("""
                    SELECT EXISTS (
                        SELECT FROM information_schema.tables 
                        WHERE table_name = 'users'
                    );
                """))
                table_exists = result.scalar()
                logger.info(f"Users table exists: {table_exists}")
                
                if not table_exists:
                    # Create users table if it doesn't exist
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
                    
                    # Check if username column exists
                    logger.info("Checking if username column exists...")
                    result = conn.execute(text("""
                        SELECT EXISTS (
                            SELECT FROM information_schema.columns 
                            WHERE table_name = 'users' 
                            AND column_name = 'username'
                        );
                    """))
                    username_exists = result.scalar()
                    logger.info(f"Username column exists: {username_exists}")
                    
                    if not username_exists:
                        logger.info("Adding username column...")
                        try:
                            conn.execute(text("""
                                ALTER TABLE users 
                                ADD COLUMN username VARCHAR UNIQUE;
                            """))
                            logger.info("Username column added successfully!")
                        except Exception as e:
                            logger.error(f"Error adding username column: {str(e)}")
                            logger.error(f"Traceback: {traceback.format_exc()}")
                            # Try without UNIQUE constraint if first attempt fails
                            try:
                                conn.execute(text("""
                                    ALTER TABLE users 
                                    ADD COLUMN username VARCHAR;
                                """))
                                logger.info("Username column added without UNIQUE constraint")
                            except Exception as e2:
                                logger.error(f"Failed to add username column: {str(e2)}")
                                logger.error(f"Traceback: {traceback.format_exc()}")
                                raise
                    
                    # Check if logs table exists
                    result = conn.execute(text("""
                        SELECT EXISTS (
                            SELECT FROM information_schema.tables 
                            WHERE table_name = 'logs'
                        );
                    """))
                    logs_exist = result.scalar()
                    logger.info(f"Logs table exists: {logs_exist}")
                    
                    if not logs_exist:
                        # Create logs table if it doesn't exist
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
                        logger.info("Logs table created successfully!")
                    else:
                        logger.info("Logs table already exists.")
                
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
                
            except SQLAlchemyError as e:
                logger.error(f"Database error: {str(e)}")
                logger.error(f"Traceback: {traceback.format_exc()}")
                raise
            
    except Exception as e:
        logger.error(f"Error during database initialization: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        sys.exit(1)

if __name__ == "__main__":
    init_db() 