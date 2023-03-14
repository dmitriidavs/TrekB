"""
TrekB | Smart Portfolio Tracker
:copyright: (c) 2023 by Dmitrii Davletshin (@dmitriidavs)
:license: Apache 2.0, see LICENSE for more details
"""

from aiogram.utils import executor

from modules.handlers import dp
from modules.bot.bot_ctx import on_startup, on_shutdown


if __name__ == '__main__':
    # TODO: move to webhook
    # start polling
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup, on_shutdown=on_shutdown)
