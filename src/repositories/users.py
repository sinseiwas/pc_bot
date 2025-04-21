from utils.repository import SQLAlchemyRepository

from db.models.users import User

class UsersRepository(SQLAlchemyRepository):
    model = User

    