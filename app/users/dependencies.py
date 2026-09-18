from datetime import datetime
from fastapi import Request, Depends
from app.exeptions import IncorrectLoginException
import jwt

from app.config import ACCESS_SECRET_KEY, ALGORITHM
from app.users.dao import UsersDAO


def get_user_token(request: Request):
    token = request.headers.get('Authorization')
    if not token:
        raise IncorrectLoginException
    return token.split('Bearer ')[-1]


async def get_user(token: str = Depends(get_user_token)):
    try:
        payload = jwt.decode(token, ACCESS_SECRET_KEY, ALGORITHM)
    except Exception as e:
        raise IncorrectLoginException
    expire: str = payload.get("exp")
    if not expire or int(expire) < datetime.utcnow().timestamp():
        raise IncorrectLoginException
    user_id: str = payload.get("sub")
    if not user_id:
        raise IncorrectLoginException
    user = await UsersDAO.find_one_or_none(id=int(user_id))
    if not user:
        raise IncorrectLoginException
    return user
