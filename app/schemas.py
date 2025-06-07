from pydantic import BaseModel, EmailStr, Field # <- pydantic is a library for data validation and settings management
from datetime import date
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
    day: str
    date: date  # <- should expect a `date`, not `None`
    week_number: int
    working_hours: float
    task_description: str
    status: str
    reviewer_id: Optional[int] = None

class LogResponse(BaseModel):
    id: int
    user_id: int
    week_number: int
    day: str
    date: Optional[date]
    working_hours: Optional[float]
    task_description: Optional[str]
    status: str
    reviewer_id: Optional[int] = None

    class Config:
        from_attributes = True

class LogUpdate(BaseModel):
    day: Optional[str] = None
    date: Optional[str] = None  # Changed to str to accept date strings
    week_number: Optional[int] = None
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