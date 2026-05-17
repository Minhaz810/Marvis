from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from auth.v1.schema import LoginRequest, Token, UserCreate, UserResponse, UserUpdate
from auth.v1.services import AuthService
from auth.v1.utils import create_access_token
from config.database import get_db

router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=201)
async def register(payload: UserCreate, db: AsyncSession = Depends(get_db)):
    return await AuthService(db).register(payload)


@router.post("/login", response_model=Token)
async def login(payload: LoginRequest, db: AsyncSession = Depends(get_db)):
    user = await AuthService(db).authenticate(payload.email, payload.password)
    return Token(access_token=create_access_token({"sub": user.id}))


@router.get("/me/{user_id}", response_model=UserResponse)
async def get_user(user_id: str, db: AsyncSession = Depends(get_db)):
    return await AuthService(db).get_by_id(user_id)


@router.patch("/me/{user_id}", response_model=UserResponse)
async def update_user(user_id: str, payload: UserUpdate, db: AsyncSession = Depends(get_db)):
    return await AuthService(db).update(user_id, payload)
