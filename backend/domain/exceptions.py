from fastapi import Request, status
from fastapi.responses import JSONResponse


class UserAlreadyExists(Exception):
    def __init__(self, email: str):
        self.email = email


def user_already_exists_handler(
    request: Request, exc: UserAlreadyExists
) -> JSONResponse:
    error_msg = f"User with {exc.email} already exists"
    return JSONResponse({"msg": error_msg}, status_code=status.HTTP_400_BAD_REQUEST)


class UserNotFound(Exception):
    def __init__(self, email: str):
        self.email = email


def user_not_found_handler(request: Request, exc: UserNotFound) -> JSONResponse:
    error_msg = f"User with email {exc.email} not found"
    return JSONResponse({"msg": error_msg}, status_code=status.HTTP_404_NOT_FOUND)


class PermissionDenied(Exception):
    pass


def permission_denied_handler(request: Request, exc: PermissionDenied) -> JSONResponse:
    return JSONResponse({"msg": "Permission denied"}, status_code=status.HTTP_403_FORBIDDEN)


class Unauthorized(Exception):
    pass


def unauthorized_handler(request: Request, exc: Unauthorized) -> JSONResponse:
    return JSONResponse({"msg": "Unauthorized"}, status_code=status.HTTP_401_UNAUTHORIZED)
