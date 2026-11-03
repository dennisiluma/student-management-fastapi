from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.security import create_access_token
from app.exceptions.base import (
    BadRequestException,
    ForbiddenException,
    InvalidCredentialsException,
    NotFoundException,
)
from app.models import User
from app.schemas.auth import LoginRequest, LoginResponse, UserRegister

password_hasher = PasswordHash.recommended()


async def register_user(db: AsyncSession, req: UserRegister) -> User:
    query = select(User).where(User.email == req.email.lower().strip())
    existing = await db.scalar(query)
    if existing:
        raise BadRequestException("User with this email address already exists")

    # Store first_name, last_name, directly on User
    user = User(
        email=req.email.lower().strip(),
        hashed_password=password_hasher.hash(req.password),
        role=req.role,
        first_name=req.first_name,
        last_name=req.last_name,
    )
    db.add(user)
    await db.commit()

    res_query = (
        select(User)
        .options(selectinload(User.classroom), selectinload(User.results))
        .where(User.id == user.id)
    )
    return await db.scalar(res_query)


async def login_user(db: AsyncSession, req: LoginRequest) -> LoginResponse:
    query = select(User).where(User.email == req.email.lower().strip())
    user = await db.scalar(query)

    if not user:
        raise NotFoundException(f"Account not found for email: {req.email}")

    if not password_hasher.verify(req.password, user.hashed_password):
        raise InvalidCredentialsException("Invalid password provided")

    if not user.is_active:
        raise ForbiddenException("User account is inactive. Please contact support")

    token = create_access_token(data={"sub": user.email})

    return LoginResponse(
        token=token,
        id=user.id,
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        role=user.role,
    )
