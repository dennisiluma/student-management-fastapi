from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.enums.enums import UserRole
from app.exceptions.base import BadRequestException, NotFoundException
from app.models import AcademicResult, User
from app.schemas.academics import AcademicResultCreate




async def create_academic_result(
    db: AsyncSession, req: AcademicResultCreate
) -> AcademicResult:
    student = await db.get(User, req.student_id)
    if not student:
        raise NotFoundException("User not found")

    if student.role != UserRole.STUDENT:
        raise BadRequestException("User is not a student")

    # Check if a result entry already exists for the given student, term, and academic year
    query = select(AcademicResult).where(
        AcademicResult.student_id == req.student_id,
        AcademicResult.term == req.term,
        AcademicResult.academic_year == req.academic_year,
    )
    result_obj = await db.scalar(query)

    if result_obj:
        # Replace existing report card grades
        result_obj.grades = req.grades
    else:
        # Instantiate a new report card entry
        result_obj = AcademicResult(
            student_id=req.student_id,
            term=req.term,
            academic_year=req.academic_year,
            grades=req.grades,
        )
        db.add(result_obj)

    await db.commit()
    await db.refresh(result_obj)
    return result_obj





async def get_my_results(
    db: AsyncSession, student_id: int
) -> List[AcademicResult]:
    """Retrieve all term result cards for a specific student ID."""
    student = await db.get(User, student_id)
    if not student:
        raise NotFoundException("Student record not found")

    query = select(AcademicResult).where(AcademicResult.student_id == student_id)
    result = await db.execute(query)
    return result.scalars().all()
