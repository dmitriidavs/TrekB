from fastapi import FastAPI
from aiogram.types import Update

from ..bot import bot
from ..creds import BOT_API_TOKEN, WEBHOOK_URL


app = FastAPI()


@app.post(f'/bot/{BOT_API_TOKEN}')
async def bot_webhook(request: Update):
    await dp.process_update(request)
    return {"ok": True}
