from aiogram.types import KeyboardButton, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


async def get_info_edit_kb():
    builder = InlineKeyboardBuilder()

    builder.row(
        InlineKeyboardButton(
        text="Изменить ссылку на вконтакте",
        callback_data="edit_vk_link"
    ),
    InlineKeyboardButton(
        text="Изменить номер телефона"
    )
    )
