from ..creds import BOT_ARCH_TYPE, BOT_ADDRESS, LOG_TYPE


async def on_startup(_) -> None:
    """Log bot on start up message"""

    print('---------------------------------------------------------\n'
          'TrekB | Smart Portfolio Tracker\n'
          ':copyright: (c) 2023 by Dmitrii Davletshin (@dmitriidavs)\n'
          ':license: Apache 2.0, see LICENSE for more details\n'
          '---------------------------------------------------------\n'
          f'Logging is in {LOG_TYPE} mode\n'
          '---------------------------------------------------------\n')
    print(f'{BOT_ARCH_TYPE} {BOT_ADDRESS} is active')


async def on_shutdown(_) -> None:
    """Log bot on shut down message"""

    print(f'{BOT_ARCH_TYPE} {BOT_ADDRESS} deactivated')
