__all__ = ['callbacks_portfolio',
           'reg_cllbcks_portfolio']

from aiogram import Dispatcher

from .callbacks_portfolio import *


def reg_cllbcks_portfolio(disp: Dispatcher) -> None:
    disp.register_callback_query_handler(cllbck_flushit_yes, text='flushit_yes')
    disp.register_callback_query_handler(cllbck_flushit_back, text='flushit_no')
