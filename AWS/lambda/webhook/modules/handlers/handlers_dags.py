from aiogram.types import Message

from ..bot import dp


@dp.message_handler(commands=['import'])
async def hndlr_start(message: Message) -> None:
    """/import command handler for importing wallet balance"""

    msg = 'Wallet balance import is not supported in Lite version :('
    await message.answer(text=msg)
    
    # gen DAG with custom params
