from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from app.users.dependencies import get_user

from app.users.models import Users
from app.categories.dao import CategoriesDAO

router = APIRouter(
    prefix="/categories",
    tags=["categories"],
)


@router.post("/add")
async def category_add(name: str, description:str = None,
                       current_user: Users = Depends(get_user)):
    if current_user.role.name != "Admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    await CategoriesDAO.add(name=name, description=description)

@router.post("/delete")
async def category_delete(category_id: int,
                          current_user: Users = Depends(get_user)):
    if current_user.role.name != "Admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    await CategoriesDAO.delete(id=category_id)

@router.post("/update")
async def category_update(category_id: int, name: str, description:str = None,
                          current_user: Users = Depends(get_user)):
    if current_user.role.name != "Admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    await CategoriesDAO.update( {'name': name,
                                 'description': description}, id=category_id)
