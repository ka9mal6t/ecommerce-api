from app.dao.base import BaseDAO
from app.order_items.models import OrderItems


class OrderItemsDAO(BaseDAO):
    model = OrderItems