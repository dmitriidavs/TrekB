"""
TrekB | Smart Portfolio Tracker
:copyright: (c) 2023 by Dmitrii Davletshin (@dmitriidavs)
:license: BSD-3-Clause, see LICENSE for more details
"""

import datetime as dt

from creds import ARCH_TYPE, BOT_ADDRESS


async def on_startup(_) -> None:
    """Log bot on start up phrase"""

    print(f'{ARCH_TYPE} bot [{BOT_ADDRESS}] activated - {dt.datetime.now()}')


async def on_shutdown(_) -> None:
    """Log bot on shut down phrase"""

    print(f'{ARCH_TYPE} bot [{BOT_ADDRESS}] deactivated - {dt.datetime.now()}')
