"""
TrekB | Smart Portfolio Tracker
:copyright: (c) 2023 by Dmitrii Davletshin (@dmitriidavs)
:license: Apache 2.0, see LICENSE for more details
"""

from aiogram.utils import executor

from bot_create import dispatcher
from handlers import register_handlers
from includes.loggers.bot_debug import on_startup, on_shutdown


if __name__ == '__main__':
    # TODO: load bot answers from seperate file to cache
    # TODO: move to webhook

    register_handlers(dispatcher)
    executor.start_polling(dispatcher, skip_updates=True, on_startup=on_startup, on_shutdown=on_shutdown)
