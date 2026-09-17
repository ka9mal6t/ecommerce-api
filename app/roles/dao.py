from app.dao.base import BaseDAO
from app.roles.models import Roles


class RolesDAO(BaseDAO):
    model = Roles