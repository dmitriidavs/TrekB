from aiogram.dispatcher.filters.state import State, StatesGroup


class FSMManualSetup(StatesGroup):
    asset_name = State()
    asset_quantity = State()


# class FSMImportWallet(StatesGroup):
#     blockchain: State()
#     wallet: State()
