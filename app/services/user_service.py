from typing import List, Optional

from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.enums.enums import UserRole
from app.exceptions.base import InvalidCredentialsException, NotFoundException
from app.models.user import User
from app.schemas.user import ChangePasswordRequest, UserProfileUpdate



password_hasher = PasswordHash.recommended()

async def get_user_profile(db: AsyncSession, current_user: User) -> User:
    query = (
        select(User)
        .options(selectinload(User.classroom), selectinload(User.results))
        .where(User.id == current_user.id)
    )
    user = await db.scalar(query)

    if not user:
        raise NotFoundException("User Not Found")
    return user




async def update_user_profile(
        db: AsyncSession, current_user: User, req: UserProfileUpdate
)-> User:
    for field, value in req.model_dump(exclude_unset=True).items():
        setattr(current_user, field, value)

    await db.commit()

    query = (
        select(User)
        .options(selectinload(User.classroom), selectinload(User.results))
        .where(User.id == current_user.id)
    )

    return await db.scalar(query)




async def get_all_users(
    db: AsyncSession, role: Optional[UserRole] = None
) -> List[User]:
    query = select(User).options(
        selectinload(User.classroom), selectinload(User.results)
    )

    if role:
        query = query.where(User.role == role)

    result = await db.execute(query)
    return result.scalars().all()



async def change_password(
    db: AsyncSession, current_user: User, req: ChangePasswordRequest
) -> None:
    # Verify the provided old password against the stored hash
    if not password_hasher.verify(req.current_password, current_user.hashed_password):
        raise InvalidCredentialsException("Current password provided is incorrect.")

    # Update with new hashed password
    current_user.hashed_password = password_hasher.hash(req.new_password)
    await db.commit()
