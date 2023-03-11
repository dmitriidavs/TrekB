# from aiogram.utils.callback_data import CallbackData
#
# from ..database.logic_portfolio import get_assets_outer, get_assets_inner


# portfolio_cd = CallbackData('get_portfolio', 'level', 'user_id', 'asset_id', 'added_at')
# edit_asset = CallbackData('user_id', 'asset_id', 'added_at')
#
#
# def create_callback_data(level: int, user_id: int, asset_id: int = 0, added_at: str = '0') -> str:
#     return portfolio_cd.new(level=level, user_id=user_id,
#                             asset_id=asset_id, added_at=added_at)
#
#
# async def assets_outer_keyboard(user_id: int) -> InlineKeyboardMarkup:
#     """Create user's assets inline keyboard"""
#
#     level = 0
#     markup = InlineKeyboardMarkup()
#
#     assets_outer = await get_assets_outer(user_id=user_id)
#     for asset in assets_outer:
#         button_text = f'{asset[1]}: {asset[2]}'
#         callback_data = create_callback_data(level=level+1,
#                                              user_id=user_id)
#         markup.add(
#             InlineKeyboardButton(text=button_text, callback_data=callback_data)
#         )
#
#     return markup
#
#
# async def assets_inner_keyboard(user_id: int, asset_id: int) -> InlineKeyboardMarkup:
#     """Create user's asset info"""
#
#     level = 1
#     markup = InlineKeyboardMarkup()
#
#     assets_inner = await get_assets_inner(user_id=user_id, asset_id=asset_id)
#     for asset_data in assets_inner:
#         button_text = f'{asset_data[1]}: {asset_data[2]} - {asset_data[3]}'
#         callback_data = create_callback_data(level=level + 1,
#                                              user_id=user_id,
#                                              asset_id=asset_data[0])
#         markup.add(
#             InlineKeyboardButton(text=button_text, callback_data=callback_data)
#         )
#     markup.row(
#         InlineKeyboardButton(text='« back', callback_data=create_callback_data(level=level-1, user_id=user_id))
#     )
#
#     return markup
#
#
# async def edit_asset_inner_keyboard(user_id: int, asset_id: int, added_at: str) -> InlineKeyboardMarkup:
#     """Edit user's asset info"""
#
#     level = 2
#     markup = InlineKeyboardMarkup()
#     markup.row(
#         InlineKeyboardButton(text='Edit quantity', callback_data=update_asset_record(col='quantity',
#                                                                                      user_id=user_id,
#                                                                                      asset_id=asset_id,
#                                                                                      added_at=added_at)),
#         InlineKeyboardButton(text='Edit date', callback_data=update_asset_record(col='added_at',
#                                                                                  user_id=user_id,
#                                                                                  asset_id=asset_id,
#                                                                                  added_at=added_at)),
#         InlineKeyboardButton(text='Delete record', callback_data=delete_asset_record(user_id=user_id,
#                                                                                      asset_id=asset_id,
#                                                                                      added_at=added_at))
#     ).add(
#         InlineKeyboardButton(text='« back', callback_data=create_callback_data(level=level-1,
#                                                                                user_id=user_id,
#                                                                                asset_id=asset_id))
#     )
#     return markup