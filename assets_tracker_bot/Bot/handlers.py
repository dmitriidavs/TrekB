import asyncio

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from includes.keyboards import *


class FSMClientSignUp(StatesGroup):
    if_sign_up = State()
    acc_config = State()


async def cmd_start(message: types.Message) -> None:
    """/start command handler"""

    msg = 'Hey, glad you\'re here!'
    await message.answer(text=msg)
    await asyncio.sleep(1)
    msg = 'I\'m your best friend when it comes to assets tracking. ' \
          'My data-driven insights will help you make the best out of your investment portfolio!'
    await message.answer(text=msg)
    await asyncio.sleep(1)
    msg = 'You can get to know me better by pressing /info. ' \
          'Or you can just go ahead and /sign_up.'
    await message.answer(text=msg)
    await asyncio.sleep(1)
    msg = 'It\'s free!'
    await message.answer(text=msg, reply_markup=kb_start)


async def cmd_info(message: types.Message) -> None:
    """/info command handler"""

    msg = 'Here is my repo: https://github.com/dmitriidavs/__portefeuille__/tree/main/assets_tracker_bot'
    await message.answer(text=msg)
    await asyncio.sleep(1)
    msg = '★ Don\'t forget to star the project ★'
    await message.answer(text=msg)


async def cmd_sign_up(message: types.Message) -> None:
    """/sign_up command handler"""

    await FSMClientSignUp.if_sign_up.set()
    msg = 'Are you sure you want to subscribe? (Y/N)'
    await message.answer(text=msg)


async def cmd_if_sign_up(message: types.Message, state: FSMContext) -> None:
    """New user auth step"""

    if message.text == 'Y':
        msg = 'All right! Let\'s sign you up.'
        await message.answer(text=msg)
        await state.finish()
    elif message.text == 'N':
        msg = 'Sorry to hear that!'
        await message.answer(text=msg)
        await state.finish()
    else:
        msg = 'Only Y/N answers accepted!'
        await message.answer(text=msg)

# TODO: add crypto wallet address for quick portfolio setup


def register_handlers(disp: Dispatcher) -> None:
    """Handlers assembly"""

    disp.register_message_handler(cmd_start, commands=['start'])
    disp.register_message_handler(cmd_info, commands=['info'])
    # disp.register_message_handler(cmd_sign_up, commands=['sign_up'], state=None)
    # disp.register_message_handler(cmd_if_sign_up, commands=['cmd_if_sign_up'], state=FSMClientSignUp.if_sign_up)
