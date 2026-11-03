from typing import List
from alembic.environment import Optional
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.deps import get_current_user
from app.db.database import get_db
from app.enums.enums import UserRole
from app.models.user import User
from app.schemas.response import ApiResponse
from app.schemas.user import ChangePasswordRequest, UserProfileUpdate, UserResponse
from app.services.user_service import (
    get_all_users,
    get_user_profile,
    update_user_profile,
    change_password,
)

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", status_code=status.HTTP_200_OK)
async def get_my_profile(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> ApiResponse[UserResponse]:
    """Get the authenticated user's profile details."""
    user = await get_user_profile(db=db, current_user=current_user)
    return ApiResponse(
        status=status.HTTP_200_OK,
        message="User profile retrieved successfully.",
        data=UserResponse.model_validate(user),
    )



@router.put("/me", status_code=status.HTTP_200_OK)
async def update_my_profile(
    body: UserProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> ApiResponse[UserResponse]:
    """Update the authenticated user's profile information."""
    user = await update_user_profile(db=db, current_user=current_user, req=body)
    return ApiResponse(
        status=status.HTTP_200_OK,
        message="Profile updated successfully.",
        data=UserResponse.model_validate(user),
    )


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_current_user)],
)
async def list_users(
    role: Optional[UserRole] = None,
    db: AsyncSession = Depends(get_db),
    _users: User = Depends(get_current_user)
) -> ApiResponse[List[UserResponse]]:
    """Retrieve all users, optionally filtered by role (e.g., /users?role=STUDENT)."""
    users = await get_all_users(db=db, role=role)
    return ApiResponse(
        status=status.HTTP_200_OK,
        message="Users list retrieved successfully.",
        data=[UserResponse.model_validate(u) for u in users],
    )


@router.put("/change-password", status_code=status.HTTP_200_OK)
async def change_user_password(
    body: ChangePasswordRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> ApiResponse[None]:
    """Change authenticated user password."""
    await change_password(db=db, current_user=current_user, req=body)
    return ApiResponse(
        status=status.HTTP_200_OK,
        message="Password updated successfully.",
        data=None,
    )