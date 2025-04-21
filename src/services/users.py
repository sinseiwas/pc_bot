from utils.repository import AbstractRepository
from utils.unitofwork import UnitOfWork
from schemas.users import AddUserSchema


class UserService:
    # def __init__(self, user_repo: AbstractRepository):
    #     self.user_repo: AbstractRepository = user_repo()
    
    async def add_user(self, uow: UnitOfWork, user: AddUserSchema):
        user_dict = user.model_dump()
        user_id = await uow.users.add_one(user_dict)
        return user_id