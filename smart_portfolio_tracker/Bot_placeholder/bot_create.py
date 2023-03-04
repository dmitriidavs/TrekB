"""
TrekB | Smart Portfolio Tracker
:copyright: (c) 2023 by Dmitrii Davletshin (@dmitriidavs)
:license: BSD-3-Clause, see LICENSE for more details
"""

from bot import ATCoreBot
from creds import ARCH_TYPE, API_KEY


BaseBot = ATCoreBot(ARCH_TYPE, API_KEY)
bot = BaseBot.bot
dispatcher = BaseBot.dispatcher
