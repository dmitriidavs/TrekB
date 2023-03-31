from aiogram.dispatcher.filters.state import State, StatesGroup


class FSMManualAdd(StatesGroup):
    asset_name = State()
    asset_quantity = State()


class FSMEditQuantity(StatesGroup):
    new_asset_quantity = State()


class FSMEditDate(StatesGroup):
    new_asset_date = State()


# class FSMImportWallet(StatesGroup):
#     blockchain: State()
#     wallet: State()
