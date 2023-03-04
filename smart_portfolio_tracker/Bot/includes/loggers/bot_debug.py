from includes.loggers.log_config import basic_log
from creds import BOT_ARCH_TYPE, BOT_ADDRESS


async def on_startup(_) -> None:
    """Log bot on start up message"""

    print('---------------------------------------------------------\n'
          'TrekB | Smart Portfolio Tracker\n'
          ':copyright: (c) 2023 by Dmitrii Davletshin (@dmitriidavs)\n'
          ':license: Apache 2.0, see LICENSE for more details\n'
          '---------------------------------------------------------')
    basic_log.info(f'{BOT_ARCH_TYPE} bot({BOT_ADDRESS}) is active')


async def on_shutdown(_) -> None:
    """Log bot on shut down message"""

    basic_log.info(f'{BOT_ARCH_TYPE} bot({BOT_ADDRESS}) deactivated')
