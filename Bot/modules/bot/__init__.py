__all__ = ['corebot', 'bot_ctx',
           'bot', 'dp']

from .corebot import CoreBot
from ..creds import BOT_API_TOKEN, BOT_FSM_STORAGE_TYPE, CACHE_HOST, CACHE_PORT


Bot = CoreBot(
    api_token=BOT_API_TOKEN,
    cache_host=CACHE_HOST,
    cache_port=CACHE_PORT,
    storage_type=BOT_FSM_STORAGE_TYPE
)
bot = Bot.bot
dp = Bot.dispatcher
