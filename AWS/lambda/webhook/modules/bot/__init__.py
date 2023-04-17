__all__ = ['webhookbot',
           'bot', 'dp']

from .webhookbot import WebhookBot
from ..creds import BOT_API_TOKEN


Bot = WebhookBot(api_token=BOT_API_TOKEN)
bot = Bot.bot
dp = Bot.dispatcher
