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
                    
                    # Safely add missing columns to users table
                    logger.info("Checking for missing columns in users table...")
                    existing_columns = conn.execute(text("""
                        SELECT column_name 
                        FROM information_schema.columns 
                        WHERE table_name = 'users';
                    """))
                    existing_columns = [row[0] for row in existing_columns]
                    logger.info(f"Existing columns: {existing_columns}")
                    
                    # Define required columns and their definitions
                    required_columns = {
                        'id': 'SERIAL PRIMARY KEY',
                        'email': 'VARCHAR UNIQUE NOT NULL',
                        'username': 'VARCHAR UNIQUE',
                        'hashed_password': 'VARCHAR NOT NULL',
                        'role': 'VARCHAR NOT NULL'
                    }
                    
                    # Add missing columns
                    for column, definition in required_columns.items():
                        if column not in existing_columns:
                            logger.info(f"Adding missing column: {column}")
                            try:
                                # Extract the data type and constraints from the definition
                                data_type = definition.split()[0]
                                constraints = ' '.join(definition.split()[1:])
                                
                                # Add the column with appropriate constraints
                                conn.execute(text(f"""
                                    ALTER TABLE users 
                                    ADD COLUMN {column} {data_type} {constraints};
                                """))
                                logger.info(f"Added column {column} successfully")
                            except Exception as e:
                                logger.error(f"Error adding column {column}: {str(e)}")
                                logger.error(f"Traceback: {traceback.format_exc()}")
                                # Try without constraints if the first attempt fails
                                try:
                                    conn.execute(text(f"""
                                        ALTER TABLE users 
                                        ADD COLUMN {column} {data_type};
                                    """))
                                    logger.info(f"Added column {column} without constraints")
                                except Exception as e2:
                                    logger.error(f"Failed to add column {column} even without constraints: {str(e2)}")
                                    logger.error(f"Traceback: {traceback.format_exc()}")
                
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