from typing import List

from fastapi import APIRouter, Depends, status

from sqlalchemy.ext.asyncio import AsyncSession
from app.core.deps import require_role, get_current_user
from app.db.database import get_db
from app.enums.enums import UserRole
from app.models.user import User
from app.schemas.classrooms import (
    AssignClassroomRequest,
    AssignTeacherRequest,
    ClassroomCreate,
    ClassroomResponse,
    ClassroomUpdate,
)
from app.schemas.response import ApiResponse
from app.schemas.user import UserResponse
from app.services.classroom_service import (
    assign_student_to_classroom,
    assign_teacher_to_classroom,
    create_classroom,
    get_classrooms,
    get_my_classmates,
    get_teacher_students,
    update_classroom,
)

router = APIRouter(prefix="/classrooms", tags=["Classrooms"])


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_role(UserRole.ADMIN))],
)
async def create_classroom_api(
    body: ClassroomCreate, db: AsyncSession = Depends(get_db)
) -> ApiResponse[ClassroomResponse]:

    classroom = await create_classroom(db=db, req=body)
    return ApiResponse(
        status=status.HTTP_201_CREATED,
        message="Classroom created successfully.",
        data=ClassroomResponse.model_validate(classroom),
    )


@router.put(
    "",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(require_role(UserRole.ADMIN))],
)
async def edit_classroom_api(
    body: ClassroomUpdate, db: AsyncSession = Depends(get_db)
) -> ApiResponse[ClassroomResponse]:
    classroom = await update_classroom(db=db, req=body)
    return ApiResponse(
        status=status.HTTP_200_OK,
        message="Classroom updated successfully.",
        data=ClassroomResponse.model_validate(classroom),
    )


@router.get("", status_code=status.HTTP_200_OK)
async def get_all_classrooms_api(
    db: AsyncSession = Depends(get_db),
) -> ApiResponse[List[ClassroomResponse]]:
    """Retrieve all classrooms."""
    classrooms = await get_classrooms(db=db)

    return ApiResponse(
        status=status.HTTP_200_OK,
        message="Classrooms retrieved successfully.",
        data=[ClassroomResponse.model_validate(c) for c in classrooms],
    )


@router.post(
    "/assign-teacher",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(require_role(UserRole.ADMIN))],
)
async def assign_teacher_api(
    body: AssignTeacherRequest,
    db: AsyncSession = Depends(get_db),
) -> ApiResponse[ClassroomResponse]:
    """Assign a teacher to a classroom, unassigning them from any previous classroom (Admin only)."""
    classroom = await assign_teacher_to_classroom(
        db=db, classroom_id=body.classroom_id, teacher_id=body.teacher_id
    )
    return ApiResponse(
        status=status.HTTP_200_OK,
        message="Teacher assigned to classroom successfully.",
        data=ClassroomResponse.model_validate(classroom),
    )


@router.post(
    "/assign-student",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(require_role(UserRole.ADMIN))],
)
async def add_student_to_classroom_api(
    body: AssignClassroomRequest,
    db: AsyncSession = Depends(get_db),
) -> ApiResponse[UserResponse]:
    """Reassign a student user to a classroom."""
    user = await assign_student_to_classroom(db=db, body=body)
    return ApiResponse(
        status=status.HTTP_200_OK,
        message="Student assigned to classroom successfully.",
        data=user,
    )


@router.get(
    "/my-students",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(require_role(UserRole.TEACHER))],
)
async def get_my_students_api_as_a_teacher(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> ApiResponse[List[UserResponse]]:
    """Retrieve all students belonging to the classroom managed by the current teacher."""
    students = await get_teacher_students(db=db, teacher_id=current_user.id)
    return ApiResponse(
        status=status.HTTP_200_OK,
        message="Teacher's students retrieved successfully.",
        data=[UserResponse.model_validate(student) for student in students],
    )


@router.get(
    "/my-classmates",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(require_role(UserRole.STUDENT))],
)
async def get_my_classmates_data_api(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ApiResponse[List[UserResponse]]:
    # Call the service layer method explicitly via its module namespace
    classmates = await get_my_classmates(db, current_user)

    return ApiResponse(
        status=200, message="Classmates retrieved successfully.", data=classmates
    )
