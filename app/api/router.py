

from fastapi import APIRouter
from app.api.auth import router as auth_router
from app.api.users import router as users_router
from app.api.classroom import router as classroom_router
from app.api.academic import router as academic_router

api_router = APIRouter()

@api_router.get("/health")
async def health_check():
    return {
        "message":"API health is fine"
    }


api_router.include_router(auth_router)
api_router.include_router(users_router)
api_router.include_router(classroom_router)
api_router.include_router(academic_router)
