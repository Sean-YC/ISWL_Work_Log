from sqlalchemy.orm import Session
from . import models, schemas
from .auth import get_password_hash
from typing import List

def bulk_register_users(db: Session, users: List[schemas.UserCreate]):
    created_users = []
    for user_data in users:
        # check if email and username already exist
        if db.query(models.User).filter(models.User.email == user_data.email).first():
            print(f"Email {user_data.email} already exists")
            continue
        if db.query(models.User).filter(models.User.username == user_data.username).first():
            print(f"Username {user_data.username} already exists")
            continue

        # create new user
        hashed_password = get_password_hash(user_data.password)
        db_user = models.User(
            email=user_data.email,
            username=user_data.username,
            hashed_password=hashed_password,
            role=user_data.role
        )
        db.add(db_user)
        created_users.append(db_user)
    
    db.commit()
    for user in created_users:
        db.refresh(user)
    
    return created_users

# example usage
if __name__ == "__main__":
    from .database import SessionLocal
    
    # example user data
    users_to_register = [
        schemas.UserCreate(
            email="user1@example.com",
            username="user1",
            password="password123",
            role="intern"
        ),
        schemas.UserCreate(
            email="user2@example.com",
            username="user2",
            password="password123",
            role="supervisor"
        ),
    ]
    
    db = SessionLocal()
    try:
        created_users = bulk_register_users(db, users_to_register)
        print(f"Successfully registered {len(created_users)} users")
    finally:
        db.close() 