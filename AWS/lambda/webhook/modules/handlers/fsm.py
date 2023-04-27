from aiogram.dispatcher.filters.state import State, StatesGroup


class FSMImportWallet(StatesGroup):
    blockchain: State()
    wallet_address: State()
