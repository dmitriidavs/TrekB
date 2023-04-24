from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeChat


async def set_menu_commands(bot: Bot, chat_id: int):
    """
    Main bot commands that allow portfolio insights
    -----------------------------------------------
    Handled by Lambda & Airflow
    """

    return await bot.set_my_commands(
        commands=[
            BotCommand('summary', 'Show portfolio infographics'),
            BotCommand('import', 'Import balance using your wallet address'),
        ],
        scope=BotCommandScopeChat(chat_id)
    )
