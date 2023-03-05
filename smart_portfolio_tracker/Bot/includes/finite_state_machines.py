from aiogram.dispatcher.filters.state import State, StatesGroup


class FSMManualAdd(StatesGroup):
    asset_name = State()
    asset_quantity = State()


# class FSMImportWallet(StatesGroup):
#     blockchain: State()
#     wallet: State()


# class FSMFlushIt(StatesGroup):
