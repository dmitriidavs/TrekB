"""
TrekB | Smart Portfolio Tracker
:copyright: (c) 2023 by Dmitrii Davletshin (@dmitriidavs)
:license: BSD-3-Clause, see LICENSE for more details
"""

import asyncio

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from utils import *
from includes.keyboards import *
from includes.finite_state_machines import *
from includes.loggers.log import log_ux


# TODO: move interim dialogue states & bot answers to MongoDB (or Redis?)
@log_ux(btn='/start')
async def cmd_start(message: types.Message) -> None:
    """/start command handler"""

    # if user has already got a portfolio
    if await user_has_portfolio(message.from_user.id):
        msg = f'Hey, {message.from_user.first_name}, you already have a portfolio!\n' \
              'What would you like to do with it? You can:\n' \
              '/portfolio - manage it.\n' \
              '/delete - start again.'
        await message.answer(text=msg, reply_markup=kb_start_active)
    # if new user
    else:
        msg = f'Hi, {message.from_user.first_name}. I\'m TrekB. Glad to see you here!'
        await message.answer(text=msg)
        await asyncio.sleep(1)
        msg = 'I\'m your best friend when it comes to assets tracking. ' \
              'My data-driven insights will help you make the best out of your investment portfolio!'
        await message.answer(text=msg)
        await asyncio.sleep(1)
        msg = 'You can learn more about me by pressing /info. ' \
              'Or you can just go ahead and /join.'
        await message.answer(text=msg, reply_markup=kb_start)

        # save user info in user DB
        await save_user_info(**{
            'user_id': message.from_user.id,
            'user_first_name': message.from_user.first_name,
            'user_last_name': message.from_user.last_name,
            'user_username': message.from_user.username,
            'user_language_code': message.from_user.language_code,
            'user_is_premium': False if message.from_user.is_premium is None else True
        })


@log_ux(btn='/info')
async def cmd_info(message: types.Message) -> None:
    """/info command handler"""

    msg = 'Here is my repo: https://github.com/dmitriidavs/__portefeuille__/tree/main/assets_tracker_bot'
    await message.answer(text=msg)
    await asyncio.sleep(1)
    msg = '★ Don\'t forget to star the project ★'
    await message.answer(text=msg)


@log_ux(btn='/join')
async def cmd_join(message: types.Message) -> None:
    """/join command handler"""

    msg = 'All right, let\'s set you up!'
    await message.answer(text=msg)
    await asyncio.sleep(1)
    msg = 'There are 2 ways to start configuring your portfolio. You can:\n' \
          '/add - add assets by hand\n' \
          '/import - import crypto wallet balance'
    await message.answer(text=msg, reply_markup=kb_join)


@log_ux(btn='/add')
async def cmd_manual_add(message: types.Message) -> None:
    """/add command handler: start FSMManualSetup"""

    await FSMManualAdd.asset_name.set()
    msg = 'OK. Send me the ticker symbol of an asset.\n' \
          'E.g.: BTC (Bitcoin) | MSFT (Microsoft)'
    await message.answer(text=msg)


@log_ux(btn='/add', state='asset_name')
async def add_asset_name(message: types.Message, state: FSMContext) -> None:
    """
    FSMManualSetup.asset_name:
    Validating and saving name of an asset
    """
    
    async with state.proxy() as data:
        data["asset_name"] = message.text
    await FSMManualAdd.next()
    msg = 'Now send me the quantity.'
    await message.answer(text=msg)


@log_ux(btn='/add', state='asset_quantity')
async def add_asset_quantity(message: types.Message, state: FSMContext) -> None:
    """
    FSMManualSetup.asset_quantity:
    Validating and saving quantity of an asset
    """

    async with state.proxy() as data:
        data["asset_quantity"] = float(message.text)

    async with state.proxy() as data:
        msg = f'Added {data["asset_quantity"]} {data["asset_name"]} to your portfolio.'
        await message.answer(text=msg, reply_markup=kb_manual)

    await state.finish()


# async def cmd_portfolio(message: types.Message) -> None:


def register_handlers(disp: Dispatcher) -> None:
    """External handler registration for easy imports"""

    disp.register_message_handler(cmd_start, commands=['start'])
    disp.register_message_handler(cmd_info, commands=['info'])
    disp.register_message_handler(cmd_join, commands=['join'])
    disp.register_message_handler(cmd_manual_add, commands=['add'], state=None)
    disp.register_message_handler(add_asset_name, state=FSMManualAdd.asset_name)
    disp.register_message_handler(add_asset_quantity, state=FSMManualAdd.asset_quantity)
    # disp.register_message_handler(cmd_portfolio, commands=['portfolio'])
