from datetime import datetime, date
from typing import Optional, List
from enum import Enum
from pydantic import BaseModel, EmailStr


class UserRole(str, Enum):
    Admin = "Admin"
    User = "User"

class UserOut(BaseModel):
    id: int
    email: EmailStr
    role: str
    created_at: datetime

    class Config:
        from_attributes = True

class UserBase(BaseModel):
    email: EmailStr
    password: str
    role: UserRole = UserRole.User

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    current_password: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str


class StandupCreate(BaseModel):
    content: str
    date: Optional[date]

class StandupResponse(BaseModel):
    id: int
    user_id: int
    content: str
    date: date

class StandupListResponse(BaseModel):
    standups: List[StandupResponse]

class TokenData(BaseModel):
    id: Optional[int] = None

class Token(BaseModel):
    access_token: str
    type: str

    class Config:
        from_attributes = True