from random import sample

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


flushit_cllbck_bttns = (
    InlineKeyboardButton('No, back to portfolio', callback_data='flushit_no'),
    InlineKeyboardButton('Nope, nevermind', callback_data='flushit_no'),
    InlineKeyboardButton('Yes, delete my portfolio', callback_data='flushit_yes')
)


async def get_flushit_kb() -> InlineKeyboardMarkup:
    """/flushit: returns keyboard with random button order"""

    kb_flushit = InlineKeyboardMarkup()
    for clbck in sample(flushit_cllbck_bttns, len(flushit_cllbck_bttns)):
        kb_flushit.add(clbck)

    return kb_flushit
