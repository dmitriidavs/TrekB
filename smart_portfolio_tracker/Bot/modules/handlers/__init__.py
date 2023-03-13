__all__ = ['fsm', 'handlers_user', 'handlers_portfolio',
           'reg_hndlrs_user', 'reg_hndlrs_portfolio']

from aiogram import Dispatcher

from .handlers_user import *
from .handlers_portfolio import *
# from ..keyboards.callback import portfolio_cd


def reg_hndlrs_user(disp: Dispatcher) -> None:
    """User handlers registration"""

    disp.register_message_handler(hndlr_start, commands=['start'])
    disp.register_message_handler(hndlr_info, commands=['info'])
    disp.register_message_handler(hndlr_join, commands=['join'])


def reg_hndlrs_portfolio(disp: Dispatcher) -> None:
    """Portfolio handlers & callbacks registration"""

    disp.register_message_handler(hndlr_portfolio, commands=['portfolio'])
    disp.register_message_handler(hndlr_flushit, commands=['flushit'])
    disp.register_message_handler(hndlr_import, commands=['import'])
    disp.register_message_handler(hndlr_manual_add, commands=['add'], state=None)
    disp.register_message_handler(stt_asset_name, state=FSMManualAdd.asset_name)
    disp.register_message_handler(stt_asset_quantity, state=FSMManualAdd.asset_quantity)

    disp.register_callback_query_handler(cllbck_flushit_yes, text='flushit_yes')
    disp.register_callback_query_handler(cllbck_flushit_back, text='flushit_no')
    # disp.register_callback_query_handler(navigate, portfolio_cd.filter())

