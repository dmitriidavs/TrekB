from aiogram import types, Dispatcher, Bot


async def cmd_start(bot: Bot, message: types.Message) -> None:
    """/start command handler"""

    answer = 'You Take The Red Pill - You Stay In Wonderland, And I Show You How Deep The Rabbit Hole Goes.'
    await bot.send_message(message.from_user.id, answer)


def register_handlers(disp: Dispatcher) -> None:
    """Handlers assembly"""

    disp.register_message_handler(cmd_start, commands=['start'], state=None)
