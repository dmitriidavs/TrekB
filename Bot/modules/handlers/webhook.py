from fastapi import FastAPI
from aiogram import types, Dispatcher, Bot

from . import dp
from ..bot import bot
from ..creds import BOT_API_TOKEN, WEBHOOK_URL
from ..database.ddl_setup import setup_users_ddl
from ..creds import BOT_ARCH_TYPE, BOT_ADDRESS, LOG_TYPE


app = FastAPI()


@app.post(f'/bot/{BOT_API_TOKEN}')
async def bot_webhook(update: dict):
    """Process webhook update"""

    telegram_update = types.Update(**update)
    Dispatcher.set_current(dp)
    Bot.set_current(bot)
    await dp.process_update(telegram_update)


@app.on_event('startup')
async def on_startup():
    """On startup: set webhook & run init operations"""

    line_split = '\n---------------------------------------------------------\n'
    on_startup_message = [
        'TrekB | Smart Portfolio Tracker\n'
        ':copyright: (c) 2023 by Dmitrii Davletshin (@dmitriidavs)\n'
        ':license: Apache 2.0, see LICENSE for more details'
    ]

    # set webhook
    webhook_url = f'{WEBHOOK_URL}/bot/{BOT_API_TOKEN}'
    if await bot.get_webhook_info() != webhook_url:
        await bot.set_webhook(url=webhook_url)
        on_startup_message.append('Webhook has been set')

    # run DDL queries
    await setup_users_ddl()
    on_startup_message.append('Users DB schema has been set up')

    # additional info
    on_startup_message.append(f'Logging is in {LOG_TYPE} mode')
    on_startup_message.append(f'{BOT_ARCH_TYPE} {BOT_ADDRESS} is active')

    print(line_split.join(on_startup_message))


@app.on_event('shutdown')
async def on_shutdown():
    """On shutdown: remove webhook"""

    await bot.delete_webhook()
    print('Webhook has been removed\n')
    print(f'{BOT_ARCH_TYPE} {BOT_ADDRESS} deactivated')
