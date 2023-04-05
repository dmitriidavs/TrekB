from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

btn_info = KeyboardButton('/info')
btn_help = KeyboardButton('/help')
btn_join = KeyboardButton('/join')
btn_portfolio = KeyboardButton('/portfolio')
btn_flushit = KeyboardButton('/flushit')
btn_add = KeyboardButton('/add')
btn_import = KeyboardButton('/import')
btn_back = KeyboardButton('/back')


kb_start = ReplyKeyboardMarkup(resize_keyboard=True)
kb_start.row(btn_info, btn_join)

kb_start_active = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
kb_start_active. \
    insert(btn_portfolio). \
    insert(btn_add). \
    insert(btn_import). \
    insert(btn_flushit). \
    insert(btn_help)

kb_add = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb_add.row(btn_add, btn_import)

kb_manual = ReplyKeyboardMarkup(resize_keyboard=True)
kb_manual.row(btn_add, btn_portfolio, btn_help)

kb_back = ReplyKeyboardMarkup(resize_keyboard=True)
kb_back.add(btn_back)
