import re

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.schemas.auth import LoginRequest, LoginResponse, UserRegister
from app.schemas.response import ApiResponse
from app.schemas.user import UserResponse
from app.services.auth_service import login_user, register_user

router = APIRouter(prefix="/auth", tags=["Reg Login Route"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_api(
    body: UserRegister, db: AsyncSession = Depends(get_db)
) -> ApiResponse[UserResponse]:
    user = await register_user(db=db, req=body)

    return ApiResponse(
        status=status.HTTP_201_CREATED, message="Registration successful", data=user
    )



@router.post("/login", status_code=status.HTTP_200_OK)
async def login_api(body: LoginRequest, db:  AsyncSession = Depends(get_db))-> ApiResponse[LoginResponse]:
    
    login_res = await login_user(db=db, req=body);

    return ApiResponse(
        status= status.HTTP_200_OK,
        message="Login successful",
        data=login_res
    )
