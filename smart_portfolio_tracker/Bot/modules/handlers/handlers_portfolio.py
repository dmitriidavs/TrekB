from typing import Union

from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext

from .fsm import FSMManualAdd
from .handlers_user import hndlr_join
from ..database.logic_user import user_has_portfolio
from ..database.logic_portfolio import add_asset_to_portfolio
from ..validation import validate_asset_name, validate_asset_quantity
from ..keyboards.reply import kb_manual
from ..keyboards.inline import get_flushit_kb
from ..log.loggers import log_ux


@log_ux(btn='/portfolio')
async def hndlr_portfolio(message: Union[Message, CallbackQuery]) -> None:
    """/portfolio command handler for showing all the assets"""

    # if user already has a portfolio
    if await user_has_portfolio(message.from_user.id):
        msg = 'Portfolio:'
        await message.answer(text=msg)

        # if type(message) == Message:
        #     await message.answer(text=msg)
        #     await get_portfolio(message)
        # elif type(message) == CallbackQuery:
        #     await message.message.answer(text=msg)
        #     await message.answer()
    # if no portfolio: activate /join cmd
    else:
        await hndlr_join(message)


@log_ux(btn='/flushit')
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
async def hndlr_manual_add(message: Message) -> None:
    """/add command handler: start FSMManualSetup"""

    await FSMManualAdd.asset_name.set()
    msg = 'OK. Send me the ticker symbol of an asset.\n' \
          'E.g.: BTC (Bitcoin) | MSFT (Microsoft)'
    await message.answer(text=msg)


@log_ux(btn='/add', state='asset_name')
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
async def hndlr_import(message: Message) -> None:
    """/import command handler for crypto wallet balances"""

    msg = 'Wallet balance import is not supported in Lite version :('
    await message.answer(text=msg)
