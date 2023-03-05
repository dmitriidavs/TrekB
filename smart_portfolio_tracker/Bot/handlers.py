import asyncio

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from utils import *
from validation import validate_asset_name, validate_asset_quantity
from includes.keyboards import *
from includes.finite_state_machines import *
from includes.loggers.log import log_ux


@log_ux(btn='/start')
async def cmd_start(message: types.Message) -> None:
    """/start command handler"""

    # if user is already in users DB
    if await user_exists(message.from_user.id):
        # if user already has a portfolio
        if await user_has_portfolio(message.from_user.id):
            msg = f'Hey, {message.from_user.first_name}, you already have a portfolio!\n' \
                  'You can hit:\n' \
                  '/portfolio - to manage it\n' \
                  '/flushit - to start again'
            await message.answer(text=msg, reply_markup=kb_start_active)
        # if no portfolio: activate /join cmd
        else:
            await cmd_join(message)
    # if new user
    else:
        msg = f'Hi, {message.from_user.first_name}. I\'m TrekB. Glad to see you here!'
        await message.answer(text=msg)
        await asyncio.sleep(0.5)
        msg = 'You can learn more about me by pressing /info. ' \
              'Or you can just go ahead and start your portfolio by clicking /join.'
        await message.answer(text=msg, reply_markup=kb_start)

        # save user info in users DB
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

    msg = 'Here is my repo: https://github.com/dmitriidavs/__portefeuille__/tree/main/smart_portfolio_tracker'
    await message.answer(text=msg)
    await asyncio.sleep(0.5)
    msg = '★ Don\'t forget to star the project ★'
    await message.answer(text=msg)


@log_ux(btn='/join')
async def cmd_join(message: types.Message) -> None:
    """/join command handler"""

    msg = 'All right, let\'s set you up!'
    await message.answer(text=msg)
    await asyncio.sleep(0.5)
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

    if await validate_asset_name(message.text):
        async with state.proxy() as data:
            # add asset name to fsm storage
            data["asset_name"] = message.text.upper()
        # switch to next fsm state
        await FSMManualAdd.next()
        msg = 'Good. Now send me the quantity.'
        await message.answer(text=msg)
    else:
        msg = f'Can\'t find asset reference. Please try again.'
        await message.answer(text=msg)


@log_ux(btn='/add', state='asset_quantity')
async def add_asset_quantity(message: types.Message, state: FSMContext) -> None:
    """
    FSMManualSetup.asset_quantity:
    Validating and saving quantity of an asset
    """

    if await validate_asset_quantity(message.text):
        async with state.proxy() as data:
            # add asset quantity to fsm storage
            data["asset_quantity"] = float(message.text)
            # send OK reply message
            msg = f'OK. Added {data["asset_quantity"]} {data["asset_name"]} to your portfolio.'
            await message.answer(text=msg, reply_markup=kb_manual)
            # add asset to portfolio table in DB
            await add_asset_to_portfolio(user_id=message.from_user.id,
                                         asset_name=data["asset_name"],
                                         asset_quantity=data["asset_quantity"])
            # finish fsm states
            await state.finish()
    else:
        msg = f'Failed to interpret value. Please try again.'
        await message.answer(text=msg)


# TODO: when imported wallet address should be removed from dialogue in some time
@log_ux(btn='/import')
async def cmd_import(message: types.Message) -> None:
    """/import command handler for crypto wallet balances"""

    msg = 'Wallet balance import is not supported in Lite version :('
    await message.answer(text=msg)


@log_ux(btn='/portfolio')
async def cmd_portfolio(message: types.Message) -> None:
    """/portfolio command handler for showing all the assets"""

    # if user already has a portfolio
    if await user_has_portfolio(message.from_user.id):
        pass
    # if no portfolio: activate /join cmd
    else:
        await cmd_join(message)


@log_ux(btn='/flushit')
async def cmd_flushit(message: types.Message) -> None:
    """/flushit command handler for clearing portfolio"""

    pass


def register_handlers(disp: Dispatcher) -> None:
    """External handler registration for easy imports"""

    disp.register_message_handler(cmd_start, commands=['start'])
    disp.register_message_handler(cmd_info, commands=['info'])
    disp.register_message_handler(cmd_join, commands=['join'])
    disp.register_message_handler(cmd_manual_add, commands=['add'], state=None)
    disp.register_message_handler(add_asset_name, state=FSMManualAdd.asset_name)
    disp.register_message_handler(add_asset_quantity, state=FSMManualAdd.asset_quantity)
    # disp.register_message_handler(cmd_portfolio, commands=['portfolio'])
