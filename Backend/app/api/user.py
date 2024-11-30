# app/api/user.py
from fastapi import APIRouter, Depends, HTTPException, status
from typing import Optional
from app.schemas.user_schema import UserCreate, UserResponse, Token
from app.services.user_service import UserService
from app.repositories.user_repositries import UserRepository
from app.db.clickhouse_client import get_clickhouse_client
from clickhouse_driver import Client
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()

def get_user_repository(
    client: Client = Depends(get_clickhouse_client)
) -> UserRepository:
    return UserRepository(client)

def get_user_service(
    repo: UserRepository = Depends(get_user_repository)
) -> UserService:
    return UserService(repo)

@router.post("/registerUser/", response_model=UserResponse)
async def create_new_user(
    user: UserCreate,
    service: UserService = Depends(get_user_service),
):
    return service.create_user(user)

@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    service: UserService = Depends(get_user_service),
):
    user = service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    print('The User is Authenticated Now')
    access_token = service.create_access_token()
    return Token(access_token=access_token, token_type="bearer")

@router.get("/users/{email}", response_model=Optional[UserResponse])
async def get_user(
    email: str,
    service: UserService = Depends(get_user_service),
):
    return service.get_user(email)