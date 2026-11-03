from typing import List
from fastapi import APIRouter, Depends, status
from pydantic import TypeAdapter
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_current_user, require_role
from app.db.database import get_db
from app.enums.enums import UserRole
from app.models.user import User
from app.schemas.academics import AcademicResultCreate, AcademicResultResponse
from app.schemas.response import ApiResponse
from app.services.academic_service import (
    create_academic_result,
    get_my_results,
)

router = APIRouter(prefix="/results", tags=["Academic Results"])


@router.post(
    "/create",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_role(UserRole.TEACHER))],
)
async def create_academic_result_api(
    body: AcademicResultCreate,
    db: AsyncSession = Depends(get_db),
) -> ApiResponse[AcademicResultResponse]:
    """Create a new term report card containing all subject grades for a student (Teachers only)."""
    result = await create_academic_result(db=db, req=body)
    return ApiResponse(
        status=status.HTTP_201_CREATED,
        message="Term results created successfully.",
        data=AcademicResultResponse.model_validate(result),
    )


@router.get(
    "/me",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(require_role(UserRole.STUDENT))],
)
async def list_my_results_api(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> ApiResponse[List[AcademicResultResponse]]:
    """Retrieve all term report cards for the logged-in student account."""
    results = await get_my_results(db=db, student_id=current_user.id)
    return ApiResponse(
        status=status.HTTP_200_OK,
        message="Your academic results retrieved successfully.",
        data=TypeAdapter(list[AcademicResultResponse]).validate_python(results),
    )
