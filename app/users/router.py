from fastapi import APIRouter, HTTPException
from starlette import status

from app.roles.init import init_roles
from app.users.auth import create_access_token, get_password_hash, verify_password
from app.users.dao import UsersDAO
from app.roles.dao import RolesDAO

from app.users.models import Users
from app.users.schemas import SUserRegister, SUserLogin

router = APIRouter(
    prefix="/auth",
    tags=["Auth & User"]
)


@router.post("/register",
             summary="Register new user",
             description="This endpoint for register new user"
             )
async def register_user(user_data: SUserRegister):
    await init_roles()
    existing_user1 = await UsersDAO.find_one_or_none(username=user_data.username)
    existing_user2 = await UsersDAO.find_one_or_none(email=user_data.email)
    if existing_user1 or existing_user2:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, )
    role = await RolesDAO.find_one_or_none(name="User")
    await UsersDAO.add(email=user_data.email, username=user_data.username,
                              hash_password=get_password_hash(user_data.email,
                                                         user_data.password),
                       role_id=role.id)


@router.post("/login",
             summary="Login as user",
             description="This endpoint for auth as user"
             )
async def login_user(user_data: SUserLogin):
    user: Users = await UsersDAO.find_one_or_none(username=user_data.username)
    if not user or not verify_password(user.email + user_data.password, user.hash_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, )
    return {"token_type": "Bearer", 'accessToken': create_access_token({"sub": str(user.id)})}