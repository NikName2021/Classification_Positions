import asyncio
import logging
from aiogram import Dispatcher
from aiogram.filters.command import Command

from settings import *
from handlers import main_handlers
from additiional import *

# Включаем логирование, чтобы не пропустить важные сообщения
# logging.basicConfig(level=logging.INFO)
# Объект бота

dp = Dispatcher()
dp.include_routers(main_handlers.router)


@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer('Это бот классификатор', reply_markup=key_start())


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
