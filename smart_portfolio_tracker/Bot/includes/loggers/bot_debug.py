from includes.loggers.config import basic_log
from creds import BOT_ARCH_TYPE, BOT_ADDRESS


async def on_startup(_) -> None:
    """Log bot on start up phrase"""

    basic_log.info(f'{BOT_ARCH_TYPE} bot({BOT_ADDRESS}) is active')


async def on_shutdown(_) -> None:
    """Log bot on shut down phrase"""

    basic_log.info(f'{BOT_ARCH_TYPE} bot({BOT_ADDRESS}) deactivated')
