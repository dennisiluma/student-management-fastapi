

from typing import Optional

from app.enums.enums import UserRole

from .base import BaseSchema


class UserRegister(BaseSchema):
    email: str
    password: str
    role: UserRole = UserRole.STUDENT
    first_name: Optional[str] = None
    last_name: Optional[str] = None



class LoginRequest(BaseSchema):
    email: str
    password: str




class LoginResponse(BaseSchema):
    token: str
    id: int
    email: str
    role: UserRole
    first_name: Optional[str] = None
    last_name: Optional[str] = None