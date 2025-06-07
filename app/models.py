from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date, Float, Time
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String)  # e.g., intern, supervisor, admin
    username = Column(String, unique=True, index=True)

class Log(Base):
    __tablename__ = 'logs'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date = Column(Date, nullable=False)
    start_time = Column(Time, nullable=False)  # Required start time ("in")
    working_hours = Column(Float, nullable=False)  # Required hours
    task_description = Column(String, nullable=False)  # Required task description
    status = Column(String, default="pending")  # Keep for review logic, not required in form
    reviewer_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # Keep for review logic, not required in form
