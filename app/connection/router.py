from fastapi import APIRouter, Depends
from app.users.dependencies import get_user

from app.users.models import Users

router = APIRouter(
    prefix="/connection",
    tags=["Connection"]
)


@router.get("/ping",
            summary="Test connection",
            description="This endpoint for test connection"
            )
async def ping() -> str:
    return "pong"

@router.get("/hello",
            summary="Test connection",
            description="This endpoint for closed test connection")
async def stats_matches(current_user: Users = Depends(get_user)):
     return f"hello {current_user.username}"
