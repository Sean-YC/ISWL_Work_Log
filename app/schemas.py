from pydantic import BaseModel, EmailStr, Field
from datetime import date, time
from typing import Optional, List
from enum import Enum

# ============ Log Status Enum ============
class LogStatus(str, Enum):
    """Enum for log status values"""
    APPROVED = "approved"
    PENDING = "pending"
    REJECTED = "rejected"

# ============ User Schemas ============
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: str = "intern"

class UserOut(BaseModel):
    id: int
    username: str
    email: str
    role: str

    model_config = {
        "from_attributes": True
    }

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str | None = None
    role: str | None = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

# ============ Log Schemas ============

class LogCreate(BaseModel):
    date: date
    start_time: time
    end_time: time
    task_description: str
    # status 和 reviewer_id 由後端自動設置，前端不需要傳送

class LogResponse(BaseModel):
    id: int
    user_id: int
    date: date
    start_time: time
    end_time: time
    task_description: str
    status: LogStatus
    reviewer_id: Optional[int] = None

    model_config = {
        "from_attributes": True
    }

class LogUpdate(BaseModel):
    date: Optional[date] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    task_description: Optional[str] = None
    status: Optional[LogStatus] = None
    reviewer_id: Optional[int] = None

    model_config = {
        "from_attributes": True
    }

class LogSubmit(BaseModel):
    """Schema for submitting a draft log for approval"""
    status: LogStatus = LogStatus.PENDING

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[str] = None

class UserList(BaseModel):
    users: List[UserOut]

    model_config = {
        "from_attributes": True
    }

# ============ Leave Status Enum ============
class LeaveStatus(str, Enum):
    """Enum for leave status values"""
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

# ============ Leave Type Enum ============
class LeaveType(str, Enum):
    """Enum for leave type values"""
    ANNUAL_LEAVE = "annual_leave"
    SICK_LEAVE = "sick_leave"
    PERSONAL_LEAVE = "personal_leave"

# ============ Leave Schemas ============

class LeaveCreate(BaseModel):
    leave_type: LeaveType
    start_date: date
    end_date: date
    reason: str
    contact: Optional[str] = None

class LeaveResponse(BaseModel):
    id: int
    user_id: int
    leave_type: str
    start_date: date
    end_date: date
    reason: str
    contact: Optional[str] = None
    status: str
    reviewer_id: Optional[int] = None
    created_at: date

    model_config = {
        "from_attributes": True
    }

class LeaveUpdate(BaseModel):
    leave_type: Optional[LeaveType] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    reason: Optional[str] = None
    contact: Optional[str] = None
    status: Optional[LeaveStatus] = None

    model_config = {
        "from_attributes": True
    }

class LeaveBalanceResponse(BaseModel):
    user_id: int
    annual_leave: int
    sick_leave: int
    personal_leave: int

    model_config = {
        "from_attributes": True
    }