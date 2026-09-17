from app.dao.base import BaseDAO
from app.status.models import Status


class StatusDAO(BaseDAO):
    model = Status