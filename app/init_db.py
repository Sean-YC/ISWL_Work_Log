from sqlalchemy import create_engine, text
import os
import sys
from dotenv import load_dotenv
import logging
import traceback
from sqlalchemy.exc import SQLAlchemyError
from .database import Base
from .models import User, Log

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
        
        try:
            # Create all tables
            logger.info("Creating all tables...")
            Base.metadata.create_all(bind=engine)
            logger.info("All tables created successfully!")
            
            # Verify table structure
            with engine.connect() as conn:
                # Check users table
                result = conn.execute(text("""
                    SELECT column_name, data_type, is_nullable 
                    FROM information_schema.columns 
                    WHERE table_name = 'users'
                    ORDER BY ordinal_position;
                """))
                columns = [(row[0], row[1], row[2]) for row in result]
                logger.info("\nUsers table structure:")
                for col_name, data_type, nullable in columns:
                    logger.info(f"  - {col_name}: {data_type} (nullable: {nullable})")
                
                # Check logs table
                result = conn.execute(text("""
                    SELECT column_name, data_type, is_nullable 
                    FROM information_schema.columns 
                    WHERE table_name = 'logs'
                    ORDER BY ordinal_position;
                """))
                columns = [(row[0], row[1], row[2]) for row in result]
                logger.info("\nLogs table structure:")
                for col_name, data_type, nullable in columns:
                    logger.info(f"  - {col_name}: {data_type} (nullable: {nullable})")
            
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