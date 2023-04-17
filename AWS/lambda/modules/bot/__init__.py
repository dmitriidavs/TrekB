__all__ = ['webhookbot',
           'bot', 'dp']

import os

from .webhookbot import WebhookBot


Bot = WebhookBot(api_token=os.environ.get('BOT_API_TOKEN'))
bot = Bot.bot
dp = Bot.dispatcher
