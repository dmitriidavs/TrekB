"""
TrekB | Smart Portfolio Tracker
:copyright: (c) 2023 by Dmitrii Davletshin (@dmitriidavs)
:license: BSD-3-Clause, see LICENSE for more details
"""

from aiogram.dispatcher.filters.state import State, StatesGroup


class FSMManualAdd(StatesGroup):
    asset_name = State()
    asset_quantity = State()


# class FSMImportWallet(StatesGroup):
#     blockchain: State()
#     wallet: State()
