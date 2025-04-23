from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from sqlalchemy.exc import NoResultFound

from utils.unitofwork import UnitOfWork
from services.users import UserService
from handlers.registration import RegistrationStates



class MessageMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        msg: Message,
        data: Dict[str, Any]
    ) -> Any:
        uow = UnitOfWork()
        state: FSMContext = data["state"]

        try:
            if msg.text and msg.text.startswith("/registration"):
                await msg.answer("Вы уже зарегистрированы")
                return
            user = await UserService().get_user_by_tg_id(uow=uow, tg_id=msg.from_user.id)
        except NoResultFound:
            current_state = await state.get_state()
            
            if msg.text and msg.text.startswith("/registration"):
                await handler(msg, data)
                return

            if current_state is not None:
                await handler(msg, data)
                return
            
            await state.set_state(RegistrationStates.start_reg)
            await msg.answer("Вы не зарегистрированы. Давайте начнём регистрацию.\nВведите Ваше ФИО:")
            return
        

        data["uow"] = uow
        data["user"] = user

        await handler(msg, data)