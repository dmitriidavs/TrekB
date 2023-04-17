from aiogram.types import Message

from ..bot import dp


@dp.message_handler(commands=['start'])
async def hndlr_start(message: Message) -> None:
    """/start command handler"""

    await message.answer(text=f'Hello, {message.from_user.first_name}')
