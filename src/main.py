import asyncio

from core.init_bot import dp, bot, set_commands
from handlers import registration, user_operations
import middlewares

from db.models.requests import Request
from db.models.users import User
from db import db


async def main():
    await db.create_tables()

    await set_commands()

    dp.message.outer_middleware(middlewares.message_mw())
    dp.callback_query.outer_middleware(middlewares.callback_mw())

    dp.include_routers(
        registration.router,
        user_operations.router
    )
    await dp.start_polling(bot)



if __name__ == "__main__":
    asyncio.run(main())