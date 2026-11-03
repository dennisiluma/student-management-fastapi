from fastapi import status


class ApiException(Exception):

    def __init__(self, message: str, status_code: int = status.HTTP_400_BAD_REQUEST):
        self.message = message
        self.status_code = status_code
        super().__init__(message)



# --- HTTP 400 Bad Request Subclasses ---
class BadRequestException(ApiException):
    def __init__(self, message: str):
        super().__init__(message, status_code=status.HTTP_400_BAD_REQUEST)



# --- HTTP 404 Not Found Subclasses ---
class NotFoundException(ApiException):
    def __init__(self, message: str):
        super().__init__(message, status_code=status.HTTP_404_NOT_FOUND)





# --- HTTP 403 Forbidden Subclasses. I.e when the token is valid but the user is not permitted to acces the route(I know know who you are but you should not be accessing this api route) ---
class ForbiddenException(ApiException):
    def __init__(self, message: str):
        super().__init__(message, status_code=status.HTTP_403_FORBIDDEN)

class InvalidCredentialsException(ApiException):
    def __init__(self, message: str):
        super().__init__(message, status_code=status.HTTP_400_BAD_REQUEST)

# --- HTTP 401 Unauthorized Subclasses. I.e when the token is not valid(I do not know who you are) ---
class UnauthorizedException(ApiException):
    def __init__(self, message: str):
        super().__init__(message, status_code=status.HTTP_401_UNAUTHORIZED)



class JWTException(ApiException):
    def __init__(self, message: str):
        super().__init__(message, status_code=status.HTTP_401_UNAUTHORIZED)


