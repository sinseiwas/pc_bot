from utils.repository import SQLAlchemyRepository

from db.models.requests import Request


class RequestsRepository(SQLAlchemyRepository):
    model = Request
