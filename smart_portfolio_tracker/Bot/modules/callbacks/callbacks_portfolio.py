from aiogram.types import CallbackQuery

from ..database.logic_portfolio import delete_portfolio
from ..handlers.handlers_portfolio import hndlr_portfolio
from ..keyboards.reply import kb_start
from ..log.loggers import log_ux


@log_ux(btn='/flushit', clbck='yes')
async def cllbck_flushit_yes(callback: CallbackQuery) -> None:
    """/flushit -> yes: callback deletes user's portfolio"""

    records_num = await delete_portfolio(user_id=callback.from_user.id)
    msg = f'Okey, removed your portfolio, {records_num} records in total.'
    await callback.message.answer(text=msg, reply_markup=kb_start)
    await callback.answer()


@log_ux(btn='/flushit', clbck='no')
async def cllbck_flushit_back(callback: CallbackQuery) -> None:
    """/flushit -> no: callback brings user back to portfolio"""

    # TODO: add remove prev bot's msg with callbacks
    await hndlr_portfolio(callback)
