import asyncio
from aiogram import types, Dispatcher#, Bot


async def cmd_start(message: types.Message) -> None:
    """/start command handler"""

    answer = f'Check out available commands above!'
    await message.answer(text=answer)


async def cmd_wtfru(message: types.Message) -> None:
    """/wtfru command handler"""

    answer = 'You can read about me here: https://github.com/dmitriidavs/__portefeuille__/tree/main/assets_tracker_bot'
    await message.answer(text=answer)
    await asyncio.sleep(1)
    await message.answer(text='★ Don\'t forget to star the project ★')


def register_handlers(disp: Dispatcher) -> None:
    """Handlers assembly"""

    disp.register_message_handler(cmd_start, commands=['start'])
    disp.register_message_handler(cmd_wtfru, commands=['wtfru'])
