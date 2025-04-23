from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Message

from utils.unitofwork import UnitOfWork
from services.users import UserService

from sqlalchemy.exc import NoResultFound


class CallbackMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        callback: Message,
        data: Dict[str, Any]
    ) -> Any:
        uow = UnitOfWork()

        try:
            user = await UserService().get_user_by_tg_id(uow=uow, tg_id=callback.from_user.id)
            data["user"] = user
        except NoResultFound:
            await callback.answer("Для использования бота необходимо зарегистрироваться")

        data["uow"] = uow

        await handler(callback, data)