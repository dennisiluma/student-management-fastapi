from typing import Generic, Optional, TypeVar
from .base import BaseSchema



T = TypeVar("T")

class ApiResponse(BaseSchema, Generic[T]):

    status: int
    message: str
    data: Optional[T] = None