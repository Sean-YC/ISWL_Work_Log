from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

load_dotenv()

# Get DATABASE_URL from environment variable
DATABASE_URL = os.getenv("DATABASE_URL")

def init_db():
    print("Initializing database...")
    engine = create_engine(DATABASE_URL)
    
    # 创建 users 表（如果不存在）
    with engine.connect() as conn:
        # 检查表是否存在
        result = conn.execute(text("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = 'users'
            );
        """))
        table_exists = result.scalar()
        
        if not table_exists:
            print("Creating users table...")
            conn.execute(text("""
                CREATE TABLE users (
                    id SERIAL PRIMARY KEY,
                    email VARCHAR UNIQUE NOT NULL,
                    username VARCHAR UNIQUE,
                    hashed_password VARCHAR NOT NULL,
                    role VARCHAR NOT NULL
                );
            """))
            print("Users table created successfully!")
        else:
            print("Users table already exists.")
            
            # 检查 username 列是否存在
            result = conn.execute(text("""
                SELECT EXISTS (
                    SELECT FROM information_schema.columns 
                    WHERE table_name = 'users' AND column_name = 'username'
                );
            """))
            column_exists = result.scalar()
            
            if not column_exists:
                print("Adding username column...")
                conn.execute(text("""
                    ALTER TABLE users ADD COLUMN username VARCHAR UNIQUE;
                """))
                print("Username column added successfully!")
            else:
                print("Username column already exists.")
        
        conn.commit()
    
    print("Database initialization completed!")

if __name__ == "__main__":
    init_db() 