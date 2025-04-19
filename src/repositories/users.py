from utils.repository import SQLAlchemyRepository

from db.models.users import User

class UserRepository(SQLAlchemyRepository):
    model = User

    