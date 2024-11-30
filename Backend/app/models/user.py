from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    mobile_number: str
    password: str
    name: str

class User(BaseModel):
    id: int
    email: str
    username: str
    mobile_number: str
    hashed_password: str
    created_at: datetime
    updated_at: datetime

    class Config:
        arbitrary_types_allowed = True  # Allow arbitrary types such as datetime
        orm_mode = True  # To allow ORM compatibility