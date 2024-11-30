# app/repositories/user_repository.py
from datetime import datetime
from typing import Dict, Optional
from fastapi import HTTPException, Depends
from app.db.clickhouse_client import get_clickhouse_client
from clickhouse_driver import Client
from passlib.context import CryptContext
from app.schemas.user_schema import UserCreate
from app.models.user import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserRepository:
    def __init__(self, client: Client = Depends(get_clickhouse_client)):
        self.client = client
        self.ensure_tables()

    def ensure_tables(self):
        try:
            self.client.execute("""
                CREATE TABLE IF NOT EXISTS users (
                   id UInt32,
                   email String,
                   username String,
                   mobile_number String,
                   name String,
                   password_hash String,
                   is_active UInt8,
                   created_at DateTime,
                   PRIMARY KEY (id, email, username)
                ) 
                ENGINE = MergeTree()
                ORDER BY (id, email, username);
            """)
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to initialize database tables: {str(e)}"
            )

    def hash_password(self, password: str) -> str:
        try:
            return pwd_context.hash(password)
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to hash password: {str(e)}"
            )

    def check_existing_user(self, email: str, username: str) -> None:
        try:
            result = self.client.execute(
                "SELECT 1 FROM users WHERE email = %(email)s LIMIT 1",
                {"email": email}
            )
            if result:
                raise HTTPException(
                    status_code=400,
                    detail="User with this email already exists."
                )

            result = self.client.execute(
                "SELECT 1 FROM users WHERE username = %(username)s LIMIT 1",
                {"username": username.lower()}
            )
            if result:
                raise HTTPException(
                    status_code=400,
                    detail="Username already taken."
                )
        except HTTPException:
            raise  # Re-raise client-side errors
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error checking existing user: {str(e)}"
            )

    def create_user(self, user_data: Dict) -> Dict:
        try:
            self.client.execute("""
                INSERT INTO users (
                    email, username, mobile_number, name, 
                    password_hash, is_active, created_at
                ) VALUES (
                    %(email)s, %(username)s, %(mobile_number)s, 
                    %(name)s, %(password_hash)s, %(is_active)s, 
                    %(created_at)s
                )
            """, user_data)

            return {
                key: value for key, value in user_data.items() 
                if key != "password_hash"
            }
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to create user: {str(e)}"
            )

    def get_user_by_email(self, email: str) -> Optional[Dict]:
        try:
            result = self.client.execute("""
                SELECT 
                    email, username, mobile_number, name, 
                    is_active, created_at
                FROM users 
                WHERE email = %(email)s
                LIMIT 1
            """, {"email": email})

            if not result:
                return None

            return dict(zip(
                ["email", "username", "mobile_number", "name", 
                 "is_active", "created_at"],
                result[0]
            ))
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to fetch user by email: {str(e)}"
            )

    def get_user_by_username(self, username: str) -> Optional[User]:
        try:
            result = self.client.execute("""
                SELECT 
                    id, email, username, mobile_number, password_hash, created_at, created_at 
                FROM users
                WHERE username = %(username)s
                LIMIT 1
            """, {"username": username})

            if not result:
                return None

            user_data = result[0]
            return User(
                id=user_data[0],
                email=user_data[1],
                username=user_data[2],
                mobile_number=user_data[3],
                hashed_password=user_data[4],
                created_at=user_data[5],
                updated_at=user_data[6]
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to fetch user by username: {str(e)}"
            )