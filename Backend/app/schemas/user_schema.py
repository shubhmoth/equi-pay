# app/schemas/user_schema.py
from datetime import datetime
from pydantic import BaseModel, EmailStr, constr

class UserCreate(BaseModel):
    username: constr(min_length=3, max_length=30)  # type: ignore
    email: EmailStr
    mobile_number: str
    name: str
    password: str

class UserResponse(BaseModel):
    username: str
    email: EmailStr
    mobile_number: str
    name: str
    is_active: bool
    created_at: datetime

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
