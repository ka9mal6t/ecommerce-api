from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from app.order_items.dao import OrderItemsDAO
from app.users.dependencies import get_user

from app.users.models import Users
from app.orders.dao import OrdersDAO

router = APIRouter(
    prefix="/order_items",
    tags=["order_items"],
)


@router.post("/add")
async def order_item_add(order_id: int, product_id: int, quantity: int, current_user: Users = Depends(get_user)):
    order = await OrdersDAO.find_one_or_none(id=order_id, user_id=current_user.id)
    if order is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,)
    await OrderItemsDAO.add(order_id=order_id, product_id=product_id, quantity=quantity)

@router.post("/delete")
async def order_item_delete(order_item_id: int, current_user: Users = Depends(get_user)):
    order = await OrdersDAO.find_one_or_none(id=order_item_id, user_id=current_user.id)
    if order is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, )
    await OrderItemsDAO.delete(id=order_item_id)

@router.post("/update")
async def order_item_update(order_item_id: int, product_id: int, quantity: int,
                         current_user: Users = Depends(get_user)):
    order_item = await OrdersDAO.find_one_or_none(id=order_item_id, user_id=current_user.id)
    if order_item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, )
    order = await OrdersDAO.find_one_or_none(id=order_item.order_id, user_id=current_user.id)
    if order is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, )
    await OrderItemsDAO.update( {'id': order_item_id,
                               'order_id': order.id,
                               'product_id': product_id,
                               'quantity': quantity,
                                }, id=order_item_id)
