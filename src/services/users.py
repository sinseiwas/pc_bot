# from utils.repository import AbstractRepository
from utils.unitofwork import UnitOfWork
from schemas.users import AddUserSchema, UserFullSchema


class UserService:
    # def __init__(self, user_repo: AbstractRepository):
    #     self.user_repo: AbstractRepository = user_repo()
    
    async def add_user(self, uow: UnitOfWork, user: AddUserSchema):
        async with uow:
            user_dict = user.model_dump()
            user_id = await uow.users.add_one(user_dict)
            await uow.commit()
            return user_id

    async def edit_user(self, uow: UnitOfWork, id: int, user: AddUserSchema):
        async with uow:
            user_dict = user.model_dump()
            user_id = await uow.users.edit_one(id=id, data=user_dict)
            await uow.commit()
            return user_id
    
    async def get_user_by_tg_id(self, uow: UnitOfWork, tg_id: int) -> UserFullSchema:
        async with uow:
            user = await uow.users.find_one(tg_id=tg_id)
            await uow.session.close()
            return user

    async def get_user(self, uow: UnitOfWork, id: int):
        async with uow:
            user = await uow.users.find_one(id)
            return user