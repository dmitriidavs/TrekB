from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


# command buttons to react to
b1 = KeyboardButton('/info')
b2 = KeyboardButton('/sign_up')

# keyboard setups
kb_start = ReplyKeyboardMarkup(resize_keyboard=True)
kb_start.row(b1, b2)

