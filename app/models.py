from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date, DateTime, Float, Time
from sqlalchemy.orm import relationship
from datetime import date as date_type
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
    start_time = Column(Time, nullable=False)  # Required start time
    end_time = Column(Time, nullable=False)  # Required end time
    task_description = Column(String, nullable=False)  # Required task description
    status = Column(String, default="pending")  # Keep for review logic, not required in form
    reviewer_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # Keep for review logic, not required in form

class Leave(Base):
    __tablename__ = 'leaves'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    leave_type = Column(String, nullable=False)  # annual_leave, sick_leave, personal_leave
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    reason = Column(String, nullable=False)
    contact = Column(String, nullable=True)  # Contact during leave
    status = Column(String, default="pending")  # pending, approved, rejected
    reviewer_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(Date, nullable=False)  # Date when request was created

class LeaveBalance(Base):
    __tablename__ = 'leave_balances'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    annual_leave = Column(Integer, default=10)  # Annual leave balance
    sick_leave = Column(Integer, default=5)  # Sick leave balance
    personal_leave = Column(Integer, default=5)  # Personal leave balance
