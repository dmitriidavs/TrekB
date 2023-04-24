from aiogram import Bot
from aiogram.types import BotCommand


async def setup_menu_commands(bot: Bot):
    """
    Main bot commands that allow portfolio insights
    -----------------------------------------------
    Handled by Lambda & Airflow
    """

    return await bot.set_my_commands(
        commands=[
            BotCommand('summary', 'Show portfolio infographics'),
            BotCommand('import', 'Import balance using your wallet address'),
        ]
    )
