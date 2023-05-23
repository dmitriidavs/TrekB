from fastapi import FastAPI
from aiogram import types, Dispatcher, Bot

from . import dp
from ..bot import bot
from ..creds import BOT_API_TOKEN, WEBHOOK_URL


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
    """Set webhook on startup"""

    webhook_url = f'{WEBHOOK_URL}/bot/{BOT_API_TOKEN}'
    if await bot.get_webhook_info() != webhook_url:
        await bot.set_webhook(url=webhook_url)


@app.on_event('shutdown')
async def on_shutdown():
    """Remove webhook on shutdown"""

    await bot.delete_webhook()
