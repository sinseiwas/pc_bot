import asyncio

from core.init_bot import dp, bot

from handlers import registration

from db.models.requests import Request
from db.models.users import User
from db import db

async def main():
    await db.create_tables()

    dp.include_routers(
        registration.router,

    )
    await dp.start_polling(bot)



if __name__ == "__main__":
    asyncio.run(main())