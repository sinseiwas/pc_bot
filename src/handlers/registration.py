from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from schemas.users import AddUserSchema
from repositories.users import UsersRepository
from utils.unitofwork import UnitOfWork
from services.users import UserService
router = Router()


class RegistrationStates(StatesGroup):
    fullname = State()
    phone_number = State()
    vk_link = State()


@router.message(Command("start"))
async def start_msg(msg: Message, state: FSMContext):
    await msg.answer("Приветствуем тебя в телеграмм боте Пресс-центра ППОО ПетрГУ!")
    await msg.answer(
        "Для регистрации в боте введите своё ФИО"
    )
    await state.set_state(RegistrationStates.fullname)


@router.message(RegistrationStates.fullname)
async def add_fullname(msg: Message, state: FSMContext):
    await state.update_data(fullname=msg.text)
    await state.set_state(RegistrationStates.vk_link)
    await msg.answer(
        "Теперь отправьте ссылку на вашу страницу в Вконтакте"
    )


@router.message(RegistrationStates.vk_link)
async def add_link(msg: Message, state: FSMContext):
    await state.update_data(vk_link=msg.text)
    await state.set_state(RegistrationStates.phone_number)
    await msg.answer(
        "Теперь отправьте ваш номер телефона в формате +7XXXXXXXXXX"
    )


@router.message(RegistrationStates.phone_number)
async def add_phone(msg: Message, uow: UnitOfWork, state: FSMContext):
    await state.update_data(phone_number=msg.text)
    data = await state.get_data()
    try:
        user = AddUserSchema(
            tg_id=msg.from_user.id,
            tg_username=msg.from_user.username,
            tg_fullname=msg.from_user.full_name,
            fullname=data["fullname"],
            phone_number=data["phone_number"],
            vk_link=data["vk_link"]
        )

        await UserService().add_user(uow=uow, user=user)

        await state.clear()

        await msg.answer("Регистрация завершена! Спасибо за предоставленные данные.")
    except ValueError as e:
        print(
            f"Произошла ошибка: {e}"
        )
        await msg.answer(
            "Неверный формат номера. Ожидается 12 чисел.\nВведите номер в формате +7XXXXXXXXXX"
            )