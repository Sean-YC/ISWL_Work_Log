from pydantic import BaseModel, EmailStr # <- pydantic is a library for data validation and settings management
from datetime import date
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr # <- email is a string that is a valid email address
    password: str

class UserOut(BaseModel):
    id: int
    email: str

    model_config = {
        "from_attributes": True # <- this is a configuration option that allows the model to be converted to a dictionary
    }

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str | None = None

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