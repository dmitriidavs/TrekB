from asyncio import sleep as aiosleep
from aiogram.types import Message, ParseMode

from ..bot import dp
from ..database.logic_user import *
from ..keyboards.reply import *
from ..log.loggers import log_ux


@log_ux(btn='/start')
@dp.message_handler(commands=['start'])
async def hndlr_start(message: Message) -> None:
    """/start command handler"""

    # if user is already in users DB
    if await user_exists(message.from_user.id):
        # if user has already got a portfolio
        if await user_has_portfolio(message.from_user.id):
            msg = f'{message.from_user.first_name}, you already have a portfolio!\n' \
                  'You can hit:\n' \
                  ' • /portfolio - to manage portfolio\n' \
                  ' • /add - to add new assets\n' \
                  ' • /import - to import wallet balance\n' \
                  ' • /flushit - to remove portfolio\n' \
                  ' • /help - to see all capabilities'
            await message.answer(text=msg, reply_markup=kb_manual)
        # if no portfolio: activate /join cmd
        else:
            await hndlr_join(message)
    # if new user
    else:
        msg = f'Hi, {message.from_user.first_name}. I\'m TrekB. Glad to see you here!'
        await message.answer(text=msg)
        await aiosleep(0.5)
        msg = 'You can learn more about me by pressing /info. ' \
              'Or you can just go ahead and start your portfolio by clicking /join.'
        await message.answer(text=msg, reply_markup=kb_start)

        # save user info in users DB
        await save_user_info(**{
            'user_id': message.from_user.id,
            'user_first_name': message.from_user.first_name,
            'user_last_name': message.from_user.last_name,
            'user_username': message.from_user.username,
            'user_language_code': message.from_user.language_code,
            'user_is_premium': False if message.from_user.is_premium is None else True
        })


@log_ux(btn='/info')
@dp.message_handler(commands=['info'])
async def hndlr_info(message: Message) -> None:
    """/info command handler"""

    msg = f'{message.from_user.first_name}, follow the link to learn more: https://github.com/dmitriidavs/TrekB'
    await message.answer(text=msg)
    await aiosleep(0.5)
    msg = '★ Don\'t forget to star the project ★'
    await message.answer(text=msg)


@log_ux(btn='/join')
@dp.message_handler(commands=['join'])
async def hndlr_join(message: Message) -> None:
    """/join command handler"""

    msg = 'Let\'s set you up!'
    await message.answer(text=msg)
    await aiosleep(0.5)
    msg = 'There are 2 ways to start configuring your portfolio. You can:\n' \
          '/add - add your assets by hand\n' \
          '/import - import your crypto wallet balance'
    await message.answer(text=msg, reply_markup=kb_add)


@log_ux(btn='/help')
@dp.message_handler(commands=['help'])
async def hndlr_help(message: Message) -> None:
    """/help command handler"""

    msg = '_PORTFOLIO COMMANDS:_\n' \
          ' • /portfolio - manage portfolio\n' \
          ' • /add - add new assets\n' \
          ' • /import - import wallet balance\n' \
          ' • /flushit - remove portfolio\n' \
          '_GENERAL COMMANDS:_\n' \
          ' • /help - you\'re here\n' \
          ' • /info - project information'
    await message.answer(text=msg, parse_mode=ParseMode.MARKDOWN)
