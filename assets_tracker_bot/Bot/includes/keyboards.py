from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


start_1 = KeyboardButton('/info')
start_2 = KeyboardButton('/join')

kb_start = ReplyKeyboardMarkup(resize_keyboard=True)
kb_start.row(start_1, start_2)

join_1 = KeyboardButton('/manual')
join_2 = KeyboardButton('/import')

kb_join = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb_join.row(join_1, join_2)
