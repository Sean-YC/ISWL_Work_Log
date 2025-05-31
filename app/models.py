from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date, Float
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String)  # e.g., intern, supervisor, admin

class Log(Base):
    __tablename__ = 'logs'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    week_number = Column(Integer, nullable=False)
    day = Column(String, nullable=False)  # e.g., Monday, Tuesday
    date = Column(Date, nullable=True)    # Optional
    working_hours = Column(Float, nullable=True)
    task_description = Column(String, nullable=True)
    status = Column(String, default="pending")  # pending / approved / rejected
    reviewer_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # Who reviewed
