import json

import asyncio
from aiogram import Bot
from aiogram.types import Update

from modules.handlers import dp
from modules.creds import WEBHOOK_URL


async def main(event):
    """
    Convert AWS Lambda event to an update & handle it
    """

    Bot.set_current(dp.bot)
    update = Update.to_object(event)
    await dp.process_update(update)

    return {
        'statusCode': 200,
        'body': json.dumps({'url': WEBHOOK_URL})
    }


def lambda_handler(event, context) -> str:
    """AWS Lambda handler"""

    return asyncio.get_event_loop().run_until_complete(main(event))
