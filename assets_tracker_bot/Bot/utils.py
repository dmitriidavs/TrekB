import datetime as dt

from includes.creds import BOT_ARCH_TYPE, BOT_ADDRESS


async def on_startup(_) -> None:
    """Log bot on start up phrase"""

    print(f'{BOT_ARCH_TYPE} bot [{BOT_ADDRESS}] activated - {dt.datetime.now()}')


async def on_shutdown(_) -> None:
    """Log bot on shut down phrase"""

    print(f'{BOT_ARCH_TYPE} bot [{BOT_ADDRESS}] deactivated - {dt.datetime.now()}')
