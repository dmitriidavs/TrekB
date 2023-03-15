from aiogram.utils.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from ..database.logic_portfolio import get_assets_outer, get_assets_inner


portfolio_cd = CallbackData('list_portfolio', 'level', 'user_id', 'asset_id',
                            'ticker_symbol', 'quantity', 'added_at')


def create_cllbck_data(level: int, user_id: int, asset_id: int = 0, ticker_symbol: str = '_ticker',
                       quantity: float = 0, added_at: str = '_datetime') -> str:
    return portfolio_cd.new(level=level, user_id=user_id, asset_id=asset_id, ticker_symbol=ticker_symbol,
                            quantity=quantity, added_at=added_at)


async def assets_outer_keyboard(user_id: int) -> InlineKeyboardMarkup:
    """Create user's portfolio inline keyboard"""

    curr_level = 0
    markup = InlineKeyboardMarkup()

    assets_outer = await get_assets_outer(user_id=user_id)
    # create a button for each asset in portfolio and add it to markup
    for asset in assets_outer:
        asset_id = asset[0]
        ticker_symbol = asset[1]
        quantity_sum = asset[2]
        button_text = '{quantity:.4f}{token:^10s}'.format(token=ticker_symbol, quantity=quantity_sum)
        cllbck_data = create_cllbck_data(level=curr_level+1, user_id=user_id,
                                         asset_id=asset_id, ticker_symbol=ticker_symbol)
        markup.add(
            InlineKeyboardButton(text=button_text, callback_data=cllbck_data)
        )

    return markup


async def assets_inner_keyboard(user_id: int, asset_id: int, ticker_symbol: str) -> InlineKeyboardMarkup:
    """Create user's asset history inline keyboard"""

    curr_level = 1
    markup = InlineKeyboardMarkup()

    assets_inner = await get_assets_inner(user_id=user_id, asset_id=asset_id)
    # create a button for each asset's record in portfolio and add it to markup
    for asset_data in assets_inner:
        asset_id = asset_data[0]
        quantity = asset_data[1]
        added_dt = asset_data[2]
        button_text = f'+{quantity} | {added_dt}'
        cllbck_data = create_cllbck_data(level=curr_level+1,
                                         user_id=user_id,
                                         asset_id=asset_id,
                                         ticker_symbol=ticker_symbol,
                                         quantity=quantity,
                                         added_at=added_dt.replace(':', '+'))
        markup.add(
            InlineKeyboardButton(text=button_text, callback_data=cllbck_data)
        )
    markup.add(
        InlineKeyboardButton(text='« back', callback_data=create_cllbck_data(level=curr_level-1,
                                                                             user_id=user_id))
    )

    return markup


async def edit_asset_keyboard(user_id: int, asset_id: int, ticker_symbol: str,
                              quantity: float, added_at: str) -> InlineKeyboardMarkup:
    """Edit user's asset history inline keyboard"""

    curr_level = 2
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton(text='Edit quantity', callback_data=create_cllbck_data(level=curr_level+1,
                                                                                    user_id=user_id,
                                                                                    asset_id=asset_id,
                                                                                    ticker_symbol=ticker_symbol,
                                                                                    quantity=quantity,
                                                                                    added_at=added_at)),
        InlineKeyboardButton(text='Edit date', callback_data=create_cllbck_data(level=curr_level+2,
                                                                                user_id=user_id,
                                                                                asset_id=asset_id,
                                                                                ticker_symbol=ticker_symbol,
                                                                                quantity=quantity,
                                                                                added_at=added_at))
    )
    markup.add(
        InlineKeyboardButton(text='« back', callback_data=create_cllbck_data(level=curr_level-1,
                                                                             user_id=user_id,
                                                                             ticker_symbol=ticker_symbol,
                                                                             asset_id=asset_id))
    )
    return markup
