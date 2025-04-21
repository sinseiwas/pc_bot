from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker
)
from sqlalchemy.orm import DeclarativeBase
from contextlib import asynccontextmanager


from core import config


engine = create_async_engine(
    url=config.settings.DATABASE_URL_asyncpg,
    echo=False,
)

SessionFactory = async_sessionmaker(
    bind=engine,
    autocommit=False,
    expire_on_commit=True,
    class_=AsyncSession,
    autoflush=False,
)


@asynccontextmanager
async def get_session():
    async with SessionFactory() as session:
        yield session
        await session.commit()


class Base(DeclarativeBase):
    pass


async def create_tables():
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)