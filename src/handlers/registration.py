from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from schemas.users import AddUserSchema, UserFullSchema
from repositories.users import UsersRepository
from utils.unitofwork import UnitOfWork
from services.users import UserService
router = Router()


class RegistrationStates(StatesGroup):
    start_reg = State()
    fullname = State()
    phone_number = State()
    vk_link = State()


@router.message(Command("registration"))
async def registration(msg: Message, state: FSMContext):
    await msg.answer("Введите Ваше ФИО")
    await state.set_state(RegistrationStates.fullname)


@router.message(RegistrationStates.start_reg)
async def start_reg(msg: Message, state: FSMContext):
    await msg.answer("Введите Ваше ФИО")
    await state.set_state(RegistrationStates.fullname)

@router.message(RegistrationStates.fullname)
async def add_fullname(msg: Message, state: FSMContext):
    user_fullname = msg.text

    await state.update_data(fullname=msg.text)
    await state.set_state(RegistrationStates.vk_link)
    
    await msg.answer(
        "Теперь отправьте ссылку на вашу страницу в Вконтакте"
    )


@router.message(RegistrationStates.vk_link)
async def add_link(msg: Message, state: FSMContext):
    user_vk_link = msg.text

    await state.update_data(vk_link=user_vk_link)
    await state.set_state(RegistrationStates.phone_number)

    await msg.answer(
        "Теперь отправьте ваш номер телефона в формате +7XXXXXXXXXX"
    )


@router.message(RegistrationStates.phone_number)
async def add_phone(msg: Message, uow: UnitOfWork, state: FSMContext):
    user_phone_number = msg.text

    await state.update_data(phone_number=user_phone_number)
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
    except:
        await msg.answer(
            "При регистрации произошла ошибка"
        )
