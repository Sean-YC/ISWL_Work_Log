from pydantic import BaseModel, EmailStr, Field # <- pydantic is a library for data validation and settings management
from datetime import date, time
from typing import Optional, List

class UserCreate(BaseModel):
    username: str  # Username is required for registration
    email: EmailStr # <- email is a string that is a valid email address
    password: str
    role: str = "intern"  # Default role is intern

class UserOut(BaseModel):
    id: int
    username: str  # Include username in user output
    email: str
    role: str

    model_config = {
        "from_attributes": True # <- this is a configuration option that allows the model to be converted to a dictionary
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

#=========== Log Schemas ============

class LogCreate(BaseModel):
    date: date  # Required
    start_time: time  # Required ("in")
    working_hours: float  # Required ("hours")
    task_description: str  # Required
    status: str
    reviewer_id: Optional[int] = None

class LogResponse(BaseModel):
    id: int
    user_id: int
    date: date  # Required
    start_time: time  # Required
    working_hours: float  # Required
    task_description: str  # Required
    status: str
    reviewer_id: Optional[int] = None

    class Config:
        from_attributes = True

class LogUpdate(BaseModel):
    date: Optional[date] = None
    start_time: Optional[time] = None
    working_hours: Optional[float] = None
    task_description: Optional[str] = None
    status: Optional[str] = None
    reviewer_id: Optional[int] = None

    class Config:
        from_attributes = True
        json_encoders = {
            date: lambda v: v.isoformat() if v else None
        }

class UserUpdate(BaseModel):
    username: Optional[str] = None  # Allow updating username
    email: Optional[EmailStr] = None
    role: Optional[str] = None

class UserList(BaseModel):
    users: List[UserOut]

    model_config = {
        "from_attributes": True
    }