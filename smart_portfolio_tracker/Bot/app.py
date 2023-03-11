"""
TrekB | Smart Portfolio Tracker
:copyright: (c) 2023 by Dmitrii Davletshin (@dmitriidavs)
:license: Apache 2.0, see LICENSE for more details
"""

from aiogram.utils import executor

from modules.bot.bot_create import dispatcher
from modules.handlers import reg_hndlrs_user, reg_hndlrs_portfolio
from modules.callbacks import reg_cllbcks_portfolio
from modules.bot.bot_ctx import on_startup, on_shutdown


if __name__ == '__main__':
    # register handlers & callbacks
    reg_hndlrs_user(dispatcher)
    reg_hndlrs_portfolio(dispatcher)
    reg_cllbcks_portfolio(dispatcher)

    # TODO: move to webhook
    # start polling
    executor.start_polling(dispatcher, skip_updates=True, on_startup=on_startup, on_shutdown=on_shutdown)
