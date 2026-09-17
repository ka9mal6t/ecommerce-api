from app.dao.base import BaseDAO
from app.categories.models import Categories

class CategoriesDAO(BaseDAO):
    model = Categories