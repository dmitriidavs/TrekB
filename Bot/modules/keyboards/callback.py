from random import sample

from aiogram.utils.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from ..database.logic_portfolio import get_assets_outer, get_assets_inner
from ..validation.formatters import format_float_to_currency, format_dt
from ..broker import broker


portfolio_cd = CallbackData('list_portfolio', 'level', 'sub_level',
                            'user_id', 'asset_id', 'ticker_symbol',
                            'quantity', 'added_at')


def create_cllbck_data(level: int, user_id: int, sub_level: int = -1,
                       asset_id: int = -1, ticker_symbol: str = '_ticker_err',
                       quantity: float = -1, added_at: str = '_dt_err') -> str:
    return portfolio_cd.new(level=level, sub_level=sub_level, user_id=user_id, asset_id=asset_id,
                            ticker_symbol=ticker_symbol, quantity=quantity, added_at=added_at)


async def assets_outer_keyboard(user_id: int) -> InlineKeyboardMarkup:
    """Create user's portfolio inline keyboard"""

    curr_level = 0
    markup = InlineKeyboardMarkup(row_width=2)

    assets_outer = await get_assets_outer(user_id=user_id)
    # create a button for each asset in portfolio and add it to markup
    for asset in assets_outer:
        asset_id = asset[0]
        ticker_symbol = asset[1]
        quantity_sum = asset[2]
        # format quanity sum as currency
        quantity_sum_text = await format_float_to_currency(quantity_sum, 4)
        # create callback data & add button
        button_text = f'{quantity_sum_text}   {ticker_symbol}'
        cllbck_data = create_cllbck_data(level=curr_level+1, user_id=user_id,
                                         asset_id=asset_id, ticker_symbol=ticker_symbol)
        markup.insert(
            InlineKeyboardButton(text=button_text,
                                 callback_data=cllbck_data)
        )

    return markup


async def assets_inner_keyboard(user_id: int, asset_id: int, ticker_symbol: str) -> InlineKeyboardMarkup:
    """Create user's asset history inline keyboard"""

    curr_level = 1
    sub_level = -1
    markup = InlineKeyboardMarkup()

    assets_inner = await get_assets_inner(user_id=user_id, asset_id=asset_id)
    # create a button for each asset's record in portfolio and add it to markup
    for asset_data in assets_inner:
        asset_id = asset_data[0]
        quantity = asset_data[1]
        added_at = asset_data[2]
        # format quanity sum as currency & added_at as date
        quantity_text = await format_float_to_currency(quantity, 4)
        added_at_text = await format_dt(added_at)
        # create callback data & add button
        button_text = f'+{quantity_text} | {added_at_text}'
        cllbck_data = create_cllbck_data(level=curr_level+1,
                                         user_id=user_id,
                                         asset_id=asset_id,
                                         ticker_symbol=ticker_symbol,
                                         quantity=quantity,
                                         added_at=added_at.replace(':', '+'))
        markup.add(
            InlineKeyboardButton(text=button_text,
                                 callback_data=cllbck_data)
        )
    markup.row(
        InlineKeyboardButton(text='« back',
                             callback_data=create_cllbck_data(level=curr_level-1,
                                                              user_id=user_id)),
        InlineKeyboardButton(text='× delete',
                             callback_data=create_cllbck_data(level=curr_level,
                                                              sub_level=sub_level+1,
                                                              asset_id=asset_id,
                                                              ticker_symbol=ticker_symbol,
                                                              user_id=user_id))
    )

    return markup


async def edit_asset_keyboard(user_id: int, asset_id: int, ticker_symbol: str,
                              quantity: float, added_at: str) -> InlineKeyboardMarkup:
    """Edit user's asset history inline keyboard"""

    curr_level = 2
    sub_level = -1
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton(text='Edit quantity',
                             callback_data=create_cllbck_data(level=curr_level,
                                                              sub_level=sub_level+1,
                                                              user_id=user_id,
                                                              asset_id=asset_id,
                                                              ticker_symbol=ticker_symbol,
                                                              quantity=quantity,
                                                              added_at=added_at)),
        InlineKeyboardButton(text='Edit date',
                             callback_data=create_cllbck_data(level=curr_level,
                                                              sub_level=sub_level+2,
                                                              user_id=user_id,
                                                              asset_id=asset_id,
                                                              ticker_symbol=ticker_symbol,
                                                              quantity=quantity,
                                                              added_at=added_at))
    ).add(
        InlineKeyboardButton(text='× delete record', callback_data=create_cllbck_data(level=curr_level,
                                                                                      sub_level=sub_level+3,
                                                                                      user_id=user_id,
                                                                                      asset_id=asset_id,
                                                                                      ticker_symbol=ticker_symbol,
                                                                                      quantity=quantity,
                                                                                      added_at=added_at))
    ).add(
        InlineKeyboardButton(text='« back', callback_data=create_cllbck_data(level=curr_level-1,
                                                                             user_id=user_id,
                                                                             ticker_symbol=ticker_symbol,
                                                                             asset_id=asset_id))
    )
    return markup


async def delete_asset_history_keyboard(user_id: int, asset_id: int, ticker_symbol: str) -> InlineKeyboardMarkup:
    """Delete user's asset inline keyboard with buttons in random order"""

    curr_level = 1
    sub_level = 0
    markup = InlineKeyboardMarkup()

    delete_asset_cllbck_bttns = (
        InlineKeyboardButton(text='No, back to activity',
                             callback_data=create_cllbck_data(level=curr_level,
                                                              user_id=user_id,
                                                              asset_id=asset_id,
                                                              ticker_symbol=ticker_symbol)),
        InlineKeyboardButton(text='Yes, delete asset data',
                             callback_data=create_cllbck_data(level=curr_level,
                                                              sub_level=sub_level+1,
                                                              user_id=user_id,
                                                              asset_id=asset_id,
                                                              ticker_symbol=ticker_symbol)),
        InlineKeyboardButton(text='Nope, back to portfolio',
                             callback_data=create_cllbck_data(level=curr_level-1,
                                                              user_id=user_id))
    )

    for clbck in sample(delete_asset_cllbck_bttns, len(delete_asset_cllbck_bttns)):
        markup.add(clbck)

    return markup


async def delete_record_keyboard(user_id: int, asset_id: int, ticker_symbol: str,
                                 quantity: float, added_at: str) -> InlineKeyboardMarkup:
    """Delete user's asset record inline keyboard with buttons in random order"""

    curr_level = 2
    sub_level = 2
    markup = InlineKeyboardMarkup()

    delete_record_cllbck_bttns = (
        InlineKeyboardButton(text='No, back to record',
                             callback_data=create_cllbck_data(level=curr_level,
                                                              user_id=user_id,
                                                              asset_id=asset_id,
                                                              ticker_symbol=ticker_symbol,
                                                              quantity=quantity,
                                                              added_at=added_at)),
        InlineKeyboardButton(text='Yes, delete record data',
                             callback_data=create_cllbck_data(level=curr_level,
                                                              sub_level=sub_level+1,
                                                              user_id=user_id,
                                                              asset_id=asset_id,
                                                              ticker_symbol=ticker_symbol,
                                                              quantity=quantity,
                                                              added_at=added_at)),
        InlineKeyboardButton(text='Nope, back to portfolio',
                             callback_data=create_cllbck_data(level=curr_level-2,
                                                              user_id=user_id))
    )

    for clbck in sample(delete_record_cllbck_bttns, len(delete_record_cllbck_bttns)):
        markup.add(clbck)

    return markup
