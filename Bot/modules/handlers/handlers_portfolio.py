from typing import Union

from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext
from aiogram.types.message import ParseMode

from .fsm import FSMManualAdd, FSMEditQuantity, FSMEditDate
from .handlers_user import hndlr_join
from ..bot import dp
from ..database.logic_user import user_has_portfolio
from ..database.logic_portfolio import (
    ticker_symbol_is_valid,
    add_asset_to_portfolio,
    delete_portfolio,
    delete_asset_from_portfolio,
    delete_record_from_portfolio,
    cache_set_asset_editing_data,
    cache_get_asset_editing_data,
    cache_del_asset_editing_data,
    update_asset_record_data
)
from ..validation import (
    validate_text_is_positive_float,
    validate_date_format
)
from ..validation.formatters import format_float_to_currency, format_dt
from ..keyboards.reply import (
    kb_manual,
    kb_start,
    kb_back
)
from ..keyboards.inline import get_flushit_kb
from ..keyboards.callback import (
    portfolio_cd,
    assets_outer_keyboard,
    assets_inner_keyboard,
    edit_asset_keyboard,
    delete_asset_history_keyboard,
    delete_record_keyboard
)
from ..log.loggers import log_ux


@dp.message_handler(commands=['back'], state='*')
async def hndlr_back(message: Message, state: FSMContext) -> None:
    """/back command handler for backing out of states"""

    curr_state = await state.get_state()
    if curr_state is not None:
        await state.finish()
        await message.answer(text='OK', reply_markup=kb_manual)


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


@log_ux(btn='/list_portfolio')
async def list_portfolio(message: Union[Message, CallbackQuery], **kwargs) -> None:
    """List user's portfolio"""

    # remove reply keyboard & inline keyboard with portfolio callbacks
    markup = await assets_outer_keyboard(message.from_user.id)
    msg = f'{message.from_user.first_name}\'s Portfolio:'
    if isinstance(message, Message):
        await message.answer(text=msg, reply_markup=markup)
    elif isinstance(message, CallbackQuery):
        callback = message
        await callback.message.edit_text(text=msg, reply_markup=markup)


@log_ux(btn='/portfolio', clbck='asset_history')
async def list_asset_history(callback: CallbackQuery, asset_id: int, ticker_symbol: str, **kwargs) -> None:
    """/portfolio -> asset: list user's asset history"""

    markup = await assets_inner_keyboard(callback.from_user.id, asset_id, ticker_symbol)
    await callback.message.edit_text(text=f'{ticker_symbol} Activity:', reply_markup=markup)


@log_ux(btn='/portfolio', clbck='edit_asset')
async def list_asset_editing(callback: CallbackQuery, asset_id: int, ticker_symbol: str,
                             quantity: float, added_at: str, **kwargs) -> None:
    """/portfolio -> asset -> asset record: edit user's asset history"""

    markup = await edit_asset_keyboard(callback.message.from_user.id, asset_id, ticker_symbol, quantity, added_at)
    quantity_text = await format_float_to_currency(quantity, 6)
    added_at_text = await format_dt(added_at.replace('+', ':'))
    msg = f'Editing {ticker_symbol}:\n' \
          f'+{quantity_text} | {added_at_text}'
    await callback.message.edit_text(text=msg, reply_markup=markup)


@log_ux(btn='/portfolio', clbck='edit_asset_quantity')
@dp.message_handler(lambda message: 'Edit quantity' in message.text, state=None)
async def edit_record_quantity(callback: CallbackQuery, asset_id: int, ticker_symbol: str,
                               quantity: float, added_at: str, **kwargs) -> None:
    """/portfolio -> asset -> edit quantity: updates user's asset quantity"""

    # start new state
    await FSMEditQuantity.new_asset_quantity.set()

    msg = f'OK. Let\'s change {quantity} {ticker_symbol} added on ' \
          f'{added_at.replace("+", ":")}.\nWhat\'s the new quantity?'
    await callback.message.edit_text(text=msg)

    # set cache data for editing
    await cache_set_asset_editing_data({
        'user_id': callback.from_user.id,
        'asset_id': asset_id,
        'added_at': added_at
    })


@log_ux(btn='/portfolio', clbck='edit_asset_quantity', state='asset_quantity')
@dp.message_handler(state=FSMEditQuantity.new_asset_quantity)
async def stt_edit_record_quantity(message: Message, state: FSMContext) -> None:
    """
    FSMEditQuantity.asset_quantity:
    Validating and editing quantity of an asset on particular date
    """

    if await validate_text_is_positive_float(message.text):
        # get editing data from cache
        c_editing_data = await cache_get_asset_editing_data(message.from_user.id)
        # delete cached editing data
        await cache_del_asset_editing_data(message.from_user.id)

        # update asset quanity in portfolio table
        await update_asset_record_data(col='quantity',
                                       val=message.text,
                                       user_id=int(c_editing_data[b"user_id"]),
                                       asset_id=int(c_editing_data[b"asset_id"]),
                                       added_at=c_editing_data[b"added_at"].decode("utf-8").replace('+', ':'))

        # send OK reply message
        msg = f'Good! {message.text} is the new quantity.'
        await message.answer(text=msg, reply_markup=kb_manual)

        # finish fsm state
        await state.finish()
    else:
        msg = f'Failed to interpret value. Please try again or go /back.'
        await message.answer(text=msg)


@log_ux(btn='/portfolio', clbck='edit_asset_date')
@dp.message_handler(lambda message: 'Edit date' in message.text, state=None)
async def edit_record_date(callback: CallbackQuery, asset_id: int, ticker_symbol: str,
                           quantity: float, added_at: str, **kwargs) -> None:
    """/portfolio -> asset -> edit date: updates user's asset date"""

    # start new state
    await FSMEditDate.new_asset_date.set()

    msg = f'OK. Let\'s change {quantity} {ticker_symbol} added on ' \
          f'{added_at.replace("+", ":")}.\n' \
          f'Here is the format for the new date:\nYYYY-MM-DD hh:mm:ss'
    await callback.message.edit_text(text=msg)

    # set cache data for editing
    await cache_set_asset_editing_data({
        'user_id': callback.from_user.id,
        'asset_id': asset_id,
        'added_at': added_at
    })


@log_ux(btn='/portfolio', clbck='edit_asset_date', state='asset_date')
@dp.message_handler(state=FSMEditDate.new_asset_date)
async def stt_edit_record_date(message: Message, state: FSMContext) -> None:
    """
    FSMEditQuantity.asset_quantity:
    Validating and editing date of an asset record on particular date
    """

    if await validate_date_format(message.text):
        # get editing data from cache
        c_editing_data = await cache_get_asset_editing_data(message.from_user.id)
        # delete cached editing data
        await cache_del_asset_editing_data(message.from_user.id)

        # update asset quanity in portfolio table
        await update_asset_record_data(col='added_at',
                                       val=message.text,
                                       user_id=int(c_editing_data[b"user_id"]),
                                       asset_id=int(c_editing_data[b"asset_id"]),
                                       added_at=c_editing_data[b"added_at"].decode("utf-8").replace('+', ':'))

        # send OK reply message
        msg = f'Good! {message.text} is the new date.'
        await message.answer(text=msg, reply_markup=kb_manual)

        # finish fsm states
        await state.finish()
    else:
        msg = f'Failed to interpret value. Please try again or go /back.'
        await message.answer(text=msg)


@log_ux(btn='/portfolio', clbck='list_delete_asset')
@dp.message_handler(lambda message: message.text == '× delete')
async def list_delete_asset_history(callback: CallbackQuery, asset_id: int, ticker_symbol: str, **kwargs) -> None:
    """/portfolio -> asset -> delete data: ask if user wants to delete asset data"""

    markup = await delete_asset_history_keyboard(callback.message.from_user.id, asset_id, ticker_symbol)
    msg = f'You\'re about to delete all of the {ticker_symbol} history. Are you sure?'
    await callback.message.edit_text(text=msg, reply_markup=markup)


@log_ux(btn='/portfolio', clbck='delete_asset')
@dp.message_handler(lambda message: message.text == 'Yes, delete asset data')
async def delete_asset_history(callback: CallbackQuery, asset_id: int, ticker_symbol: str, **kwargs) -> None:
    """/portfolio -> asset -> delete data: yes"""

    await delete_asset_from_portfolio(callback.from_user.id, asset_id)
    msg = f'{ticker_symbol} deleted'
    await callback.answer(text=msg)
    await list_portfolio(callback)


@log_ux(btn='/portfolio', clbck='list_delete_record')
@dp.message_handler(lambda message: message.text == '× delete record')
async def list_delete_record_from_history(callback: CallbackQuery, asset_id: int, ticker_symbol: str,
                                          quantity: float, added_at: str, **kwargs) -> None:
    """/portfolio -> asset -> record -> delete data: ask if user wants to delete record data"""

    markup = await delete_record_keyboard(callback.message.from_user.id, asset_id,
                                          ticker_symbol, quantity, added_at)
    msg = f'You\'re about to delete {quantity} {ticker_symbol} ' \
          f'added on {added_at.replace("+", ":")}. Are you sure?'
    await callback.message.edit_text(text=msg, reply_markup=markup)


@log_ux(btn='/portfolio', clbck='delete_asset')
@dp.message_handler(lambda message: message.text == 'Yes, delete record data')
async def delete_record_from_history(callback: CallbackQuery, asset_id: int, ticker_symbol: str,
                                     quantity: float, added_at: str, **kwargs) -> None:
    """/portfolio -> asset -> record -> delete data: yes"""

    await delete_record_from_portfolio(callback.from_user.id, asset_id, added_at.replace('+', ':'))
    msg = f'-{quantity} {ticker_symbol} | {added_at.replace("+", ":")}'
    await callback.answer(text=msg)
    await list_asset_history(callback, asset_id, ticker_symbol)


# TODO: add caching
@dp.callback_query_handler(portfolio_cd.filter())
async def navigate(callback: CallbackQuery, callback_data: dict) -> None:
    """Assign functions for portfolio navigation"""

    curr_level = callback_data["level"]
    sub_level = callback_data["sub_level"]
    user_id = callback_data["user_id"]
    asset_id = callback_data["asset_id"]
    ticker_symbol = callback_data["ticker_symbol"]
    quantity = callback_data["quantity"]
    added_at = callback_data["added_at"]

    levels = {
        '0': {
            'main': list_portfolio,
        },
        '1': {
            'main': list_asset_history,
            '0': list_delete_asset_history,
            '1': delete_asset_history
        },
        '2': {
            'main': list_asset_editing,
            '0': edit_record_quantity,
            '1': edit_record_date,
            '2': list_delete_record_from_history,
            '3': delete_record_from_history
        }
    }

    # main func is activated if sub_level is not provided
    curr_level_function = levels[curr_level]['main'] if sub_level == '-1' else levels[curr_level][sub_level]
    await curr_level_function(callback,
                              user_id=user_id,
                              asset_id=asset_id,
                              ticker_symbol=ticker_symbol,
                              quantity=quantity,
                              added_at=added_at)


@log_ux(btn='/flushit')
@dp.message_handler(commands=['flushit'])
async def hndlr_flushit(message: Message) -> None:
    """/flushit command handler for clearing portfolio"""

    # if user already has a portfolio
    if await user_has_portfolio(message.from_user.id):
        msg = 'You\'re about to delete your portfolio. Are you sure?'
        await message.answer(text=msg,
                             reply_markup=await get_flushit_kb())
    # if no portfolio: activate /join cmd
    else:
        msg = 'You don\'t have a portfolio yet!'
        await message.answer(text=msg)
        await hndlr_join(message)


@log_ux(btn='/flushit', clbck='yes')
@dp.callback_query_handler(text='flushit_yes')
async def cllbck_flushit_yes(callback: CallbackQuery) -> None:
    """/flushit -> yes: callback deletes user's portfolio"""

    records_num = await delete_portfolio(user_id=callback.from_user.id)
    msg = f'OK, removed your portfolio, {records_num} records in total.'
    await callback.message.answer(text=msg, reply_markup=kb_start)
    await callback.answer()


@log_ux(btn='/flushit', clbck='no')
@dp.callback_query_handler(text='flushit_no')
async def cllbck_flushit_back(callback: CallbackQuery) -> None:
    """/flushit -> no: callback brings user back to portfolio"""

    await hndlr_portfolio(callback)


@log_ux(btn='/add')
@dp.message_handler(commands=['add'], state=None)
async def hndlr_manual_add(message: Message) -> None:
    """/add command handler: start FSMManualSetup"""

    await FSMManualAdd.asset_name.set()
    msg = 'OK. Send me the ticker symbol. ' \
          'Check out all of the supported assets ' \
          '<a href="https://telegra.ph/TrekB-Supported-Assets-03-23">here</a>.'
    await message.answer(text=msg, reply_markup=kb_back, parse_mode=ParseMode.HTML)


@log_ux(btn='/add', state='asset_name')
@dp.message_handler(state=FSMManualAdd.asset_name)
async def stt_asset_name(message: Message, state: FSMContext) -> None:
    """
    FSMManualSetup.asset_name:
    Validating and saving name of an asset
    """

    if await ticker_symbol_is_valid(message.text.replace(' ', '').upper()):
        async with state.proxy() as data:
            # add asset name to fsm storage
            data["asset_name"] = message.text.upper()
        # switch to next fsm state
        await FSMManualAdd.next()
        msg = 'Good. Now send me the quantity.'
        await message.answer(text=msg)
    else:
        msg = f'Can\'t find asset reference. Please try again or go /back.'
        await message.answer(text=msg)


@log_ux(btn='/add', state='asset_quantity')
@dp.message_handler(state=FSMManualAdd.asset_quantity)
async def stt_asset_quantity(message: Message, state: FSMContext) -> None:
    """
    FSMManualSetup.asset_quantity:
    Validating and saving quantity of an asset
    """

    if await validate_text_is_positive_float(message.text):
        async with state.proxy() as data:
            # add asset quantity to fsm storage
            data["asset_quantity"] = float(message.text)
            # send OK reply message
            msg = f'+{data["asset_quantity"]} {data["asset_name"]} in your portfolio.'
            await message.answer(text=msg, reply_markup=kb_manual)
            # add asset to portfolio table in DB
            await add_asset_to_portfolio(user_id=message.from_user.id,
                                         asset_name=data["asset_name"],
                                         asset_quantity=data["asset_quantity"])
            # finish fsm states
            await state.finish()
    else:
        msg = f'Failed to interpret value. Please try again or go /back.'
        await message.answer(text=msg)


# TODO: when imported wallet address should be removed from dialogue in some time
@log_ux(btn='/import')
@dp.message_handler(commands=['import'])
async def hndlr_import(message: Message) -> None:
    """/import command handler for crypto wallet balances"""

    msg = 'Wallet balance import is not supported in Lite version :('
    await message.answer(text=msg)