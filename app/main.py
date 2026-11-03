from contextlib import asynccontextmanager
import logging

from fastapi import FastAPI, Request
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from app.api.router import api_router
from app.db.database import engine
from app.exceptions.base import ApiException
from app.exceptions.handlers import api_exception_handler
from fastapi.responses import JSONResponse

logger = logging.getLogger("uvicorn.error")


@asynccontextmanager
async def lifespan(_app: FastAPI):
    try:
        # 1. Ping DB to fail fast if unreachable
        async with engine.begin() as conn:
            await conn.execute(text("SELECT 1"))
        logger.info(f" ✅ Database connection verified successfully.")

    except Exception as e:
        logger.error(f"❌ Application failed to initialize: {e}")
        raise e


    yield

    # --- SHUTDOWN ---
    logger.warning(f" ⚠️ Shutting down application...")
    try:
        await engine.dispose()
        logger.info(f" ✅ Database connection pool safely cleared.")
    except Exception as e:
        logger.error(f"❌ Error during database pool disposal: {e}")




app = FastAPI(title="Student management", version="1.0.0", lifespan=lifespan)



app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)


app.add_exception_handler(ApiException, api_exception_handler)

# # if an error is not proprely handles, it will be captured and returend ere
# @app.add_exception_handler(Exception)
# async def general_exception_handler(_request: Request, exc: Exception):
#     return JSONResponse(
#         status_code=500,
#         content={
#             "status": 500,
#             "message": "An unexpected error occurred",
#             "details": str(exc),
#         },
#     )


app.include_router(api_router, prefix="/api")


@app.get("/")
async def root():
    return {
        "message": "Welcome to School Management API",
        "version": "1.0.0",
        "docs": "/docs",
    }
