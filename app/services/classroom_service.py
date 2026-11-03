from typing import List

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
import logging
from sqlalchemy.orm import selectinload
from app.enums.enums import UserRole
from app.exceptions.base import BadRequestException, NotFoundException
from app.models import classroom
from app.models.classroom import Classroom
from app.models.user import User
from app.schemas.classrooms import (
    AssignClassroomRequest,
    ClassroomCreate,
    ClassroomUpdate,
)

logger = logging.getLogger("uvicorn.error")


async def create_classroom(db: AsyncSession, req: ClassroomCreate) -> Classroom:

    logger.info("insde create classroom")

    query = select(Classroom).where(Classroom.name == req.name)
    existing = await db.scalar(query)
    if existing:
        raise BadRequestException(f"Classroom with name '{req.name}' already exists.")

    classroom = Classroom(name=req.name)
    db.add(classroom)
    await db.commit()
    await db.refresh(classroom)

    return classroom


async def update_classroom(db: AsyncSession, req: ClassroomUpdate) -> classroom:
    classroom = await db.get(Classroom, req.id)
    if not classroom:
        raise NotFoundException("Classroom not found.")

    # Check if another classroom already uses the requested name
    query = select(Classroom).where(Classroom.name == req.name, Classroom.id != req.id)
    duplicate = await db.scalar(query)
    if duplicate:
        raise BadRequestException(f"Classroom with name '{req.name}' already exists.")

    classroom.name = req.name
    await db.commit()
    await db.refresh(classroom)
    return classroom


async def get_classrooms(db: AsyncSession) -> list[Classroom]:

    query = select(Classroom)
    result = await db.scalars(query)
    classrooms = result.all()

    if not classrooms:
        raise NotFoundException("No classrooms found")

    return classrooms


async def assign_teacher_to_classroom(
    db: AsyncSession, classroom_id: int, teacher_id: int
) -> Classroom:

    teacher = await db.get(User, teacher_id)
    if not teacher or teacher.role not in [UserRole.TEACHER]:
        raise BadRequestException("User must be a valid teacher.")

    target_classroom = await db.get(Classroom, classroom_id)
    if not target_classroom:
        raise NotFoundException("Target classroom not found.")

    await db.execute(
        update(Classroom)
        .where(Classroom.teacher_id == teacher_id)
        .values(teacher_id=None)
    )

    target_classroom.teacher_id = teacher_id
    await db.commit()
    await db.refresh(target_classroom)

    return target_classroom


async def assign_student_to_classroom(
    db: AsyncSession, body: AssignClassroomRequest
) -> User:

    user_id = body.user_id

    student = await db.get(User, user_id)
    if not student or student.role != UserRole.STUDENT:
        raise NotFoundException("Student record not found")

    classroom = await db.get(Classroom, body.classroom_id)
    if not classroom:
        raise NotFoundException("Classroom not found")

    student.classroom_id = body.classroom_id
    await db.commit()

    query = (
        select(User)
        .options(selectinload(User.classroom), selectinload(User.results))
        .where(User.id == user_id)
    )
    return await db.scalar(query)


async def get_teacher_students(db: AsyncSession, teacher_id: int) -> List[User]:
    query = (
        select(Classroom)
        .where(Classroom.teacher_id == teacher_id)
        .options(selectinload(Classroom.students))
    )
    result = await db.execute(query)
    classroom = result.scalar_one_or_none()

    if not classroom:
        return []

    return classroom.students



async def get_my_classmates(db: AsyncSession, current_user: User) -> List[User]:
    if not current_user.classroom_id:
        raise NotFoundException("You are not currently enrolled in any classroom.")

    query = select(User).where(
        User.classroom_id == current_user.classroom_id,
        User.id != current_user.id,  # Exclude self
    )
    result = await db.execute(query)
    return result.scalars().all()