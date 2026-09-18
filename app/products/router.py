from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from app.users.dependencies import get_user

from app.users.models import Users
from app.products.dao import ProductsDAO
from app.products.schemas import SProduct

router = APIRouter(
    prefix="/products",
    tags=["products"],
)


@router.post("/add")
async def product_add(product: SProduct, category_id: int = None,
                      current_user: Users = Depends(get_user)):
    if current_user.role.name != "Admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    await ProductsDAO.add(category_id=category_id, name=product.name,
                          description=product.description, price=product.price,
                          image_url=product.image_url)

@router.post("/delete")
async def product_delete(product_id: int, current_user: Users = Depends(get_user)):
    if current_user.role.name != "Admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    await ProductsDAO.delete(id=product_id)

@router.post("/update")
async def product_update(product: SProduct, category_id: int = None, current_user: Users = Depends(get_user)):
    if current_user.role.name != "Admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    await ProductsDAO.update( {'name': product.name,
                               'category_id': category_id,
                               'description': product.description,
                               'price': product.price,
                               'image_url': product.image_url
                                }, id=category_id)
