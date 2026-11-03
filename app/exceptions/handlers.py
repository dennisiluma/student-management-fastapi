from .base import ApiException

from fastapi import Request
from fastapi.responses import JSONResponse


async def api_exception_handler(request: Request, exc: ApiException) -> JSONResponse:

    return JSONResponse(
        status_code=exc.status_code,
        content={"status": exc.status_code, "message": exc.message, "data": None},
    )

