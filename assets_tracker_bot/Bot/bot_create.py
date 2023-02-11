from bot import ATCoreBot
from includes.creds import ARCH_TYPE, API_KEY


BaseBot = ATCoreBot(ARCH_TYPE, API_KEY)
bot = BaseBot.bot
dispatcher = BaseBot.dispatcher
