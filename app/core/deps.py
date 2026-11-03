from typing import Callable
import jwt
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.config import settings
from app.db.database import get_db
from app.enums.enums import UserRole
from app.exceptions.base import ForbiddenException, UnauthorizedException
from app.models.user import User

security = HTTPBearer(auto_error=False)



async def get_current_user(
        auth: HTTPAuthorizationCredentials | None = Depends(security),
        db: AsyncSession =Depends(get_db)
) -> User:
    if not auth or not auth.credentials:
        raise UnauthorizedException("Authentication token missing")

    token = auth.credentials


    try:
        payload = jwt.decode(
            token,
            settings.SECRETE_JWT_KEY,
            algorithms=[settings.ALGORITHM],
        )
        user_email: str = payload.get("sub")
        if not user_email:
            raise UnauthorizedException("Invalid token payload")

    except jwt.ExpiredSignatureError:
        raise UnauthorizedException("Token has expired")
    except jwt.PyJWTError:
        raise UnauthorizedException("Could not validate credentials")

    # Load classroom and results relationships
    query = (
        select(User)
        .options(
            selectinload(User.classroom),
            selectinload(User.results),
        )
        .where(User.email == user_email)
    )
    result = await db.execute(query)
    user = result.scalar_one_or_none()

    if not user:
        raise UnauthorizedException("User not found")

    if not user.is_active:
        raise ForbiddenException("Account is deactivated")

    return user
    



def require_role(required_role: UserRole) -> Callable:

    async def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role != required_role:
            raise ForbiddenException(
                "You do not have permission to perform this action"
            )
        return current_user

    return role_checker