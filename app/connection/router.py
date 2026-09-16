from fastapi import APIRouter

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
