from ..bot import bot
from ..database.ddl_setup import setup_users_ddl
from ..keyboards.menu import setup_menu_commands
from ..creds import BOT_ARCH_TYPE, BOT_ADDRESS, LOG_TYPE


async def on_startup(_) -> None:
    """Log bot on start up message"""

    line_split = '\n---------------------------------------------------------\n'
    on_startup_message = [
        '\nTrekB | Smart Portfolio Tracker\n'
        ':copyright: (c) 2023 by Dmitrii Davletshin (@dmitriidavs)\n'
        ':license: Apache 2.0, see LICENSE for more details'
    ]

    # run DDL queries
    await setup_users_ddl()
    on_startup_message.append('Users DB schema has been set up')
    # setup menu commands
    await setup_menu_commands(bot)
    on_startup_message.append('Menu commands have been applied')
    # additional info
    on_startup_message.append(f'Logging is in {LOG_TYPE} mode')
    on_startup_message.append(f'{BOT_ARCH_TYPE} {BOT_ADDRESS} is active')

    print(line_split.join(on_startup_message))


async def on_shutdown(_) -> None:
    """Log bot on shut down message"""

    print(f'{BOT_ARCH_TYPE} {BOT_ADDRESS} deactivated')
