from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommand

from core.config import settings

bot = Bot(
    token=settings.BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()


async def set_commands():
    commands = [
        BotCommand(command="start", description="О боте"),
        BotCommand(command="registration", description="Начать регистрацию в боте"),
        BotCommand(command="update_information", description="Обновление контактных данных"),
        BotCommand(command="make_request", description="Создать заявку об освещении")
    ]
    await bot.set_my_commands(commands)

