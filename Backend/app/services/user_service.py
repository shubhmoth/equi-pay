# app/services/user_service.py
from typing import Dict, Optional
from fastapi import HTTPException
from app.repositories.user_repositries import UserRepository
from app.schemas.user_schema import UserCreate
from datetime import datetime
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
import secrets

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def validate_username(self, username: str) -> bool:
        if not username[0].isalpha():
            raise HTTPException(
                status_code=400,
                detail="Username must start with a letter."
            )
        
        if not username.replace("_", "").replace("-", "").isalnum():
            raise HTTPException(
                status_code=400,
                detail="Username can only contain letters, numbers, underscores, and hyphens."
            )
        
        return True

    def create_user(self, user: UserCreate) -> Dict:
        self.validate_username(user.username)

        self.repository.check_existing_user(user.email, user.username)
        
        user_data = {
            "email": user.email,
            "username": user.username.lower(),
            "mobile_number": user.mobile_number,
            "name": user.name,
            "password_hash": self.repository.hash_password(user.password),
            "is_active": 1,
            "created_at": datetime.now()
        }
        
        return self.repository.create_user(user_data)

    def get_user(self, email: str) -> Optional[Dict]:
        return self.repository.get_user_by_email(email)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        print('Hey i am verifying password')
        return pwd_context.verify(plain_password, hashed_password)
    
    def authenticate_user(self, username: str, password: str):
        print('Hey i am authentiating user')
        user = self.repository.get_user_by_username(username)
        print('I got the user')
        if not user:
            return False
        if not self.verify_password(password, user.hashed_password):
            return False
        print('Hey The Password got Verified')
        return user
    
    def create_access_token(self) -> str:
        return secrets.token_urlsafe(32)