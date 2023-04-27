import requests
from aiogram.types import Message
from aiogram.dispatcher import FSMContext

from .fsm import FSMImportWallet
from ..bot import dp
from ..keyboards.callback import bc_networks_keyboard
from ..utils import create_dag_copy


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

# make a copy of a base dag with user_id ()

# activate DAG with custom params (requests)
