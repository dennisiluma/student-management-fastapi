from datetime import datetime, timedelta, timezone

from fastapi import status
import jwt

from app.core.config import settings
from app.exceptions.base import ApiException, JWTException, NotFoundException



if not all([
    settings.SECRETE_JWT_KEY, 
    settings.ALGORITHM, 
    settings.ACCESS_TOKEN_EXPIRE_DAYS
]):
    raise NotFoundException("Required JWT configuration settings are missing")


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=settings.ACCESS_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRETE_JWT_KEY, algorithm=settings.ALGORITHM)



def decode_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, settings.SECRETE_JWT_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise JWTException("Token has expired", status.HTTP_401_UNAUTHORIZED)
    except jwt.InvalidTokenError:
        raise JWTException("Invalid token", status.HTTP_401_UNAUTHORIZED)

    



