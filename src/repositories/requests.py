from src.utils.repository import SQLAlchemyRepository

from db.models.requests import Request


class RequestRepository(SQLAlchemyRepository):
    model = Request
