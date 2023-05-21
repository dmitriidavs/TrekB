import requests
from aiogram.types import Message
from aiogram.dispatcher import FSMContext

from .fsm import FSMImportWallet
from ..bot import dp
from ..keyboards.callback import bc_networks_keyboard
from ..utils import create_dag_copy
from ..creds import BUCKET_DAGS


@dp.message_handler(commands=['summary'])
async def hndlr_summary(message: Message) -> None:
    """/summary command handler for showing portfolio infographics"""

    msg = 'OK. Loading your portfolio summary.'
    await message.answer(text=msg)

    # copy base summary DAG
    create_dag_copy(BUCKET_DAGS, f'{message.from_user.id}_portfolio_summary_dag',
                    BUCKET_DAGS, 'base_portfolio_summary_dag')

    # activate DAG with custom params


# @dp.message_handler(commands=['import'], state=None)
# async def hndlr_import(message: Message) -> None:
#     """/import command handler for importing wallet balance: start FSMImportWallet"""
#
#     await FSMImportWallet.blockchain.set()
#     msg = 'OK. Firstly, choose one of the supported networks.'
#     await message.answer(text=msg, reply_markup=bc_networks_keyboard())
#
#
# @dp.message_handler(state=FSMImportWallet.blockchain)
# async def stt_blockchain(message: Message, state: FSMContext) -> None:
#     """
#     FSMImportWallet.blockchain:
#     """
