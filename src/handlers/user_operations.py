from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

# from handlers.registration import RegistrationEditStates
from schemas.users import AddUserSchema, UserFullSchema
from services.users import UserService
from utils.unitofwork import UnitOfWork


router = Router()

class RegistrationEditStates(StatesGroup):
    fullname = State()
    phone_number = State()
    vk_link = State()


@router.message(Command("update_information"))
async def edit_user_info(msg: Message, state: FSMContext):
    await msg.answer("Для смены информации о себе, пройдите регистрацию заново")
    await msg.answer("Введите своё ФИО")
    
    await state.set_state(RegistrationEditStates.fullname)


@router.message(RegistrationEditStates.fullname)
async def add_fullname(msg: Message, state: FSMContext):
    user_fullname = msg.text

    await state.update_data(fullname=msg.text)
    await state.set_state(RegistrationEditStates.vk_link)
    
    await msg.answer(
        "Теперь отправьте ссылку на вашу страницу в Вконтакте"
    )


@router.message(RegistrationEditStates.vk_link)
async def add_link(msg: Message, state: FSMContext):
    user_vk_link = msg.text

    await state.update_data(vk_link=user_vk_link)
    await state.set_state(RegistrationEditStates.phone_number)

    await msg.answer(
        "Теперь отправьте ваш номер телефона в формате +7XXXXXXXXXX"
    )


@router.message(RegistrationEditStates.phone_number)
async def add_phone(msg: Message, user: UserFullSchema, uow: UnitOfWork, state: FSMContext):
    user_phone_number = msg.text

    await state.update_data(phone_number=user_phone_number)
    data = await state.get_data()
    try:
        user_add = AddUserSchema(
            tg_id=msg.from_user.id,
            tg_username=msg.from_user.username,
            tg_fullname=msg.from_user.full_name,
            fullname=data["fullname"],
            phone_number=data["phone_number"],
            vk_link=data["vk_link"]
        )

        await UserService().edit_user(uow=uow, id=user.id, user=user_add)

        await state.clear()

        await msg.answer("Ваши данные были обновлены")
    except ValueError as e:
        print(
            f"Произошла ошибка: {e}"
        )
        await msg.answer(
            "Неверный формат номера. Ожидается 12 чисел.\nВведите номер в формате +7XXXXXXXXXX"
            )