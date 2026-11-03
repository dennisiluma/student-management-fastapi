from typing import Optional
from .base import BaseSchema



class ClassroomCreate(BaseSchema):
    name: str



class ClassroomUpdate(BaseSchema):
    id:int
    name: str


class AssignClassroomRequest(BaseSchema):
    classroom_id: int
    user_id:int


class AssignTeacherRequest(BaseSchema):
    classroom_id: int
    teacher_id: int



class ClassroomResponse(BaseSchema):
    id: int
    name: str
    teacher_id: Optional[int] = None
