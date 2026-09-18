from fastapi import HTTPException
from starlette import status

IncorrectLoginException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Incorrect email or password"
)