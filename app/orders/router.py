from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from app.products.dao import ProductsDAO
from app.users.dependencies import get_user

from app.users.models import Users
from app.status.dao import StatusDAO
from app.orders.dao import OrdersDAO

router = APIRouter(
    prefix="/orders",
    tags=["orders"],
)


@router.post("/add")
async def order_add(current_user: Users = Depends(get_user)):
    status_create = await StatusDAO.find_one_or_none(name="Created")
    if status_create is None:
        await StatusDAO.add(name="Created")
        status_create = await StatusDAO.find_one_or_none(name="Created")
    await OrdersDAO.add(user_id=current_user.id, status_id=status_create.id)

@router.post("/delete")
async def order_delete(order_id: int, current_user: Users = Depends(get_user)):
    await ProductsDAO.delete(id=order_id, user_id=current_user.id)

@router.post("/update")
async def order_update(order_id: int, new_status: str,
                         current_user: Users = Depends(get_user)):
    if current_user.role.name != "Admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    order = await OrdersDAO.find_one_or_none(id=order_id)
    status_update = await StatusDAO.find_one_or_none(name=new_status)
    if status_update is None:
        await StatusDAO.add(name=new_status)
        status_update = await StatusDAO.find_one_or_none(name=new_status)
    await ProductsDAO.update( {'id': order_id,
                               'user_id': order.user_id,
                               'status_id': status_update.id,
                               'created_at': order.created_at,
                                }, id=order_id)
