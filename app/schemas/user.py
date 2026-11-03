
from typing import Optional
from app.enums.enums import UserRole
from .base import BaseSchema


class UserProfileUpdate(BaseSchema):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None
    bio: Optional[str] = None





class UserResponse(BaseSchema):
    id: int
    email: str
    role: UserRole
    is_active: bool
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None
    bio: Optional[str] = None
    classroom_id: Optional[int] = None




class ChangePasswordRequest(BaseSchema):
    current_password: str
    new_password: str