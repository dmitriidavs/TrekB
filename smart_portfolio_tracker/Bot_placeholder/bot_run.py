"""
TrekB | Smart Portfolio Tracker
:copyright: (c) 2023 by Dmitrii Davletshin (@dmitriidavs)
:license: BSD-3-Clause, see LICENSE for more details
"""

from aiogram.utils import executor

from utils import on_startup, on_shutdown
from bot_create import dispatcher
from handlers import register_handlers


if __name__ == '__main__':
    register_handlers(dispatcher)
    executor.start_polling(dispatcher, skip_updates=True, on_startup=on_startup, on_shutdown=on_shutdown)
