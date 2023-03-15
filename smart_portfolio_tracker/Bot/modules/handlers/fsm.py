from aiogram.dispatcher.filters.state import State, StatesGroup


class FSMManualAdd(StatesGroup):
    asset_name = State()
    asset_quantity = State()


class FSMEditQuantity(StatesGroup):
    asset_quantity = State()


class FSMEditDate(StatesGroup):
    asset_date = State()


# class FSMImportWallet(StatesGroup):
#     blockchain: State()
#     wallet: State()
