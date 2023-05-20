from random import sample

from aiogram.utils.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from ..database.logic_portfolio import get_assets_outer, get_assets_inner
from ..validation.formatters import format_float_to_currency, format_dt
from .. import broker


portfolio_cd = CallbackData('list_portfolio', 'level', 'sub_level', 'user_id', 'pointer')


def create_cllbck_data(level: int, user_id: int, pointer: str = '_pointer_err', sub_level: int = -1) -> str:
    return portfolio_cd.new(level=level, sub_level=sub_level, user_id=user_id, pointer=pointer)


async def assets_outer_keyboard(user_id: int) -> InlineKeyboardMarkup:
    """Create user's portfolio inline keyboard"""

    curr_level = 0
    markup = InlineKeyboardMarkup(row_width=2)

    # request assets data from users DB
    assets_outer = await get_assets_outer(user_id=user_id)
    attributes = ('asset_id', 'ticker_symbol', 'quantity_sum')

    # add broker message & get data w/pointers
    new_broker_data = await broker.set_data(user_id=user_id, data=(assets_outer, attributes))

    # create a button for each asset in portfolio and add it to markup
    for b_data in new_broker_data:
        # create button text
        quantity_sum_text = format_float_to_currency(b_data["quantity_sum"], 4)
        button_text = f'{quantity_sum_text}   {b_data["ticker_symbol"]}'
        # create callback data
        cllbck_data = create_cllbck_data(level=curr_level+1,
                                         user_id=user_id,
                                         pointer=b_data["pointer"])
        # add button
        markup.insert(
            InlineKeyboardButton(text=button_text,
                                 callback_data=cllbck_data)
        )

    return markup


async def assets_inner_keyboard(user_id: int, broker_data: dict) -> InlineKeyboardMarkup:
    """Create user's asset history inline keyboard"""

    curr_level = 1
    sub_level = -1
    markup = InlineKeyboardMarkup()

    # request asset's records data from users DB
    assets_inner = await get_assets_inner(user_id=user_id, asset_id=broker_data["asset_id"])
    attributes = ('record_id', 'asset_id', 'ticker_symbol', 'quantity', 'added_at')

    # add broker message & get data w/pointers
    new_broker_data = await broker.set_data(user_id=user_id, data=(assets_inner, attributes))

    # create a button for each asset's record in portfolio and add it to markup
    for b_data in new_broker_data:
        # format quanity sum as currency & added_at as date
        quantity_text = format_float_to_currency(b_data["quantity"], 4)
        added_at_text = format_dt(b_data["added_at"])
        # create callback data & add button
        button_text = f'+{quantity_text} | {added_at_text}'
        cllbck_data = create_cllbck_data(level=curr_level+1,
                                         user_id=user_id,
                                         pointer=b_data["pointer"])
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
                                                              user_id=user_id,
                                                              pointer=broker_data["pointer"]))
    )

    return markup


async def edit_asset_keyboard(user_id: int, broker_data: dict) -> InlineKeyboardMarkup:
    """Edit user's asset history inline keyboard"""

    curr_level = 2
    sub_level = -1
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton(text='Edit quantity',
                             callback_data=create_cllbck_data(level=curr_level,
                                                              sub_level=sub_level+1,
                                                              user_id=user_id,
                                                              pointer=broker_data["pointer"])),
        InlineKeyboardButton(text='Edit date',
                             callback_data=create_cllbck_data(level=curr_level,
                                                              sub_level=sub_level+2,
                                                              user_id=user_id,
                                                              pointer=broker_data["pointer"]))
    ).add(
        InlineKeyboardButton(text='× delete record', callback_data=create_cllbck_data(level=curr_level,
                                                                                      sub_level=sub_level+3,
                                                                                      user_id=user_id,
                                                                                      pointer=broker_data["pointer"]))
    ).add(
        InlineKeyboardButton(text='« back', callback_data=create_cllbck_data(level=curr_level-1,
                                                                             user_id=user_id,
                                                                             pointer=broker_data["pointer"]))
    )
    return markup


async def delete_asset_history_keyboard(user_id: int, broker_data: dict) -> InlineKeyboardMarkup:
    """Delete user's asset inline keyboard with buttons in random order"""

    curr_level = 1
    sub_level = 0
    markup = InlineKeyboardMarkup()

    delete_asset_cllbck_bttns = (
        InlineKeyboardButton(text='No, back to activity',
                             callback_data=create_cllbck_data(level=curr_level,
                                                              user_id=user_id,
                                                              pointer=broker_data["pointer"])),
        InlineKeyboardButton(text='Yes, delete asset data',
                             callback_data=create_cllbck_data(level=curr_level,
                                                              sub_level=sub_level+1,
                                                              user_id=user_id,
                                                              pointer=broker_data["pointer"])),
        InlineKeyboardButton(text='Nope, back to portfolio',
                             callback_data=create_cllbck_data(level=curr_level-1,
                                                              user_id=user_id))
    )

    for clbck in sample(delete_asset_cllbck_bttns, len(delete_asset_cllbck_bttns)):
        markup.add(clbck)

    return markup


async def delete_record_keyboard(user_id: int, broker_data: dict) -> InlineKeyboardMarkup:
    """Delete user's asset record inline keyboard with buttons in random order"""

    curr_level = 2
    sub_level = 2
    markup = InlineKeyboardMarkup()

    delete_record_cllbck_bttns = (
        InlineKeyboardButton(text='No, back to record',
                             callback_data=create_cllbck_data(level=curr_level,
                                                              user_id=user_id,
                                                              pointer=broker_data["pointer"])),
        InlineKeyboardButton(text='Yes, delete record data',
                             callback_data=create_cllbck_data(level=curr_level,
                                                              sub_level=sub_level+1,
                                                              user_id=user_id,
                                                              pointer=broker_data["pointer"])),
        InlineKeyboardButton(text='Nope, back to portfolio',
                             callback_data=create_cllbck_data(level=curr_level-2,
                                                              user_id=user_id))
    )

    for clbck in sample(delete_record_cllbck_bttns, len(delete_record_cllbck_bttns)):
        markup.add(clbck)

    return markup
