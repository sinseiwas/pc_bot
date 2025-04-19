from abc import ABC, abstractmethod

from sqlalchemy import (
    insert,
    select
)

from db.db import get_session

class AbstractRepository(ABC):
    @abstractmethod
    async def add_one():
        raise NotImplementedError
    
    @abstractmethod
    async def find_all():
        raise NotImplementedError
    

class SQLAlchemyRepository(AbstractRepository):
    model = None

    async def add_one(self, data: dict) -> int:
        async with get_session() as session:
            stmt = insert(self.model).values(**data).returning(self.model.id)
            result = await session.execute(stmt)
            return result.scalar_one()

    
    async def find_all(self):
        async with get_session() as session:
            stmt = insert(self.model)
            result = await session.execute(stmt)
            result = [row[0].to_read_model() for row in result.all()]
            return result.scalar_one()