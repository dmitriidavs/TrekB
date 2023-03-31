__all__ = ['corebot', 'bot_ctx',
           'bot', 'dp']

from .corebot import CoreBot
from ..creds import BOT_API_TOKEN, BOT_FSM_STORAGE_TYPE, UTIL_DB_HOST, UTIL_DB_PORT


Bot = CoreBot(
    api_token=BOT_API_TOKEN,
    util_db_host=UTIL_DB_HOST,
    util_db_port=UTIL_DB_PORT,
    storage_type=BOT_FSM_STORAGE_TYPE
)
bot = Bot.bot
dp = Bot.dispatcher
