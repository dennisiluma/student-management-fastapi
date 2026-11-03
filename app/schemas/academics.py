from typing import Dict, Optional

from app.enums.enums import GradeTerm
from .base import BaseSchema




class AcademicResultCreate(BaseSchema):
    student_id: int
    term: GradeTerm
    academic_year: str
    grades: Dict[str, str]  # e.g. {"Maths": "A", "English": "B", "Science": "A"}



class AcademicResultResponse(BaseSchema):
    id: int
    student_id: int
    term: GradeTerm
    academic_year: str
    grades: Dict[str, str]