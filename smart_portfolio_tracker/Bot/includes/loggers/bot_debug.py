import logging

from creds import BOT_ARCH_TYPE, BOT_ADDRESS


async def on_startup(_) -> None:
    """Log bot on start up phrase"""

    logging.info(f'{BOT_ARCH_TYPE} bot ({BOT_ADDRESS}) is active')


async def on_shutdown(_) -> None:
    """Log bot on shut down phrase"""

    logging.info(f'{BOT_ARCH_TYPE} bot ({BOT_ADDRESS}) deactivated')
