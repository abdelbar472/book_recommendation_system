# app/user/schemas.py
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class SignupSchema(BaseModel):
    email: EmailStr
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=8)
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class LoginSchema(BaseModel):
    identifier: str  # email or username
    password: str
    remember_me: Optional[bool] = False


class ProfileSchema(BaseModel):
    username: str
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    bio: Optional[str] = None
    website: Optional[str] = None
    followers_count: int = 0
    following_count: int = 0

    class Config:
        from_attributes = True


class UserReadSchema(BaseModel):
    id: str
    username: str
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    bio: Optional[str] = None
    website: Optional[str] = None
    followers_count: int = 0
    following_count: int = 0
    created_at: datetime

    class Config:
        from_attributes = True


class TokenSchema(BaseModel):
    access_token: str
    token_type: str = "bearer"