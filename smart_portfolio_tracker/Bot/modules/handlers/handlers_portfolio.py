from typing import Union

from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext

from .fsm import FSMManualAdd
from .handlers_user import hndlr_join
from ..bot import dp
from ..database.logic_user import user_has_portfolio
from ..database.logic_portfolio import add_asset_to_portfolio, delete_portfolio
from ..validation import validate_asset_name, validate_asset_quantity
from ..keyboards.reply import kb_manual, kb_start
from ..keyboards.inline import get_flushit_kb
from ..keyboards.callback import (
    portfolio_cd,
    assets_outer_keyboard,
    assets_inner_keyboard
    #, edit_asset_keyboard
)
from ..log.loggers import log_ux


@log_ux(btn='/portfolio')
@dp.message_handler(commands=['portfolio'])
async def hndlr_portfolio(message: Union[Message, CallbackQuery]) -> None:
    """/portfolio command handler for showing all the assets"""

    # if user already has a portfolio
    if await user_has_portfolio(message.from_user.id):
        await list_portfolio(message)
    # if no portfolio: activate /join cmd
    else:
        await hndlr_join(message)


@log_ux(btn='/flushit', clbck='yes')
@dp.callback_query_handler(text='flushit_yes')
async def cllbck_flushit_yes(callback: CallbackQuery) -> None:
    """/flushit -> yes: callback deletes user's portfolio"""

    records_num = await delete_portfolio(user_id=callback.from_user.id)
    msg = f'Okey, removed your portfolio, {records_num} records in total.'
    await callback.message.answer(text=msg, reply_markup=kb_start)
    await callback.answer()


@log_ux(btn='/flushit', clbck='no')
@dp.callback_query_handler(text='flushit_no')
async def cllbck_flushit_back(callback: CallbackQuery) -> None:
    """/flushit -> no: callback brings user back to portfolio"""

    await callback.message.edit_text(text='', reply_markup=None)
    await hndlr_portfolio(callback)


@log_ux(btn='/list_portfolio')
async def list_portfolio(message: Union[Message, CallbackQuery], **kwargs) -> None:
    """List user's portfolio"""

    markup = await assets_outer_keyboard(message.from_user.id)
    if isinstance(message, Message):
        await message.answer(text='Portfolio:', reply_markup=markup)
    elif isinstance(message, CallbackQuery):
        callback = message
        await callback.message.edit_text(text='Portfolio:', reply_markup=markup)


@log_ux(btn='/portfolio', clbck='asset_history')
async def list_asset_history(callback: CallbackQuery, asset_id: int, **kwargs) -> None:
    """/portfolio -> asset: list user's asset history"""

    markup = await assets_inner_keyboard(callback.message.from_user.id, asset_id)
    await callback.message.edit_text(text='History:', reply_markup=markup)


# @log_ux(btn='/portfolio', clbck='asset_edit')
# async def edit_asset(callback: CallbackQuery, asset_id: int, added_at: str) -> None:
#     """/portfolio -> asset -> asset record: edit user's asset history"""
#
#     markup = await edit_asset_keyboard(callback.message.from_user.id, asset_id, added_at)
#     await callback.message.edit_text(text='Edit:', reply_markup=markup)


@dp.callback_query_handler(portfolio_cd.filter())
async def navigate(callback: CallbackQuery, cllbck_data: dict) -> None:
    """Enable portfolio navigation"""

    curr_level = cllbck_data["level"]
    user_id = cllbck_data["user_id"]
    asset_id = cllbck_data["asset_id"]
    added_at = cllbck_data["added_at"]

    levels = {
        0: list_portfolio,
        1: list_asset_history
    }

    curr_level_function = levels[curr_level]
    await curr_level_function(callback,
                              user_id=user_id,
                              asset_id=asset_id,
                              added_at=added_at)


@log_ux(btn='/flushit')
@dp.message_handler(commands=['flushit'])
async def hndlr_flushit(message: Message) -> None:
    """/flushit command handler for clearing portfolio"""

    # if user already has a portfolio
    if await user_has_portfolio(message.from_user.id):
        msg = 'You\'re about to delete your portfolio. Are you sure?'
        await message.answer(text=msg,
                             reply_markup=get_flushit_kb())
    # if no portfolio: activate /join cmd
    else:
        msg = 'You don\'t have a portfolio yet!'
        await message.answer(text=msg)
        await hndlr_join(message)


@log_ux(btn='/add')
@dp.message_handler(commands=['add'], state=None)
async def hndlr_manual_add(message: Message) -> None:
    """/add command handler: start FSMManualSetup"""

    await FSMManualAdd.asset_name.set()
    msg = 'OK. Send me the ticker symbol of an asset.\n' \
          'E.g.: BTC (Bitcoin) | MSFT (Microsoft)'
    await message.answer(text=msg)


@log_ux(btn='/add', state='asset_name')
@dp.message_handler(commands=['add'], state=FSMManualAdd.asset_name)
async def stt_asset_name(message: Message, state: FSMContext) -> None:
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
@dp.message_handler(commands=['add'], state=FSMManualAdd.asset_quantity)
async def stt_asset_quantity(message: Message, state: FSMContext) -> None:
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
@dp.message_handler(commands=['import'])
async def hndlr_import(message: Message) -> None:
    """/import command handler for crypto wallet balances"""

    msg = 'Wallet balance import is not supported in Lite version :('
    await message.answer(text=msg)
