from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton
)


start_1 = KeyboardButton('/info')
start_2 = KeyboardButton('/join')
start_active_1 = KeyboardButton('/clear')
start_active_2 = KeyboardButton('/portfolio')

kb_start = ReplyKeyboardMarkup(resize_keyboard=True)
kb_start.row(start_1, start_2)
kb_start_active = ReplyKeyboardMarkup(resize_keyboard=True)
kb_start_active.row(start_active_1, start_active_2)

join_1 = KeyboardButton('/manual')
join_2 = KeyboardButton('/import')

kb_join = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb_join.row(join_1, join_2)

manual_1 = KeyboardButton('/add')
manual_2 = KeyboardButton('/portfolio')

kb_manual = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb_manual.add(manual_1).add(manual_2)