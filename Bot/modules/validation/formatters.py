import pytz
import datetime as dt
from decimal import Decimal

from ..creds import TIMEZONE
from ..log.loggers import logger


def format_float_to_currency(val: float, max_dec: int) -> str:
    """
    Optimize float to display as currency:
    int if possible else optimal float
    """

    d = Decimal(str(val))
    # check for int
    if d == d.to_integral():
        res = d.quantize(Decimal(1))
    else:
        res = Decimal(str(round(d, max_dec))).normalize()

    def format_currency(dec: Decimal) -> str:
        return '{:,}'.format(dec)

    return format_currency(res)

def format_dt(val: str) -> str:
    return dt.datetime.strptime(
        val, '%Y-%m-%d %H:%M:%S.%f'
    ).strftime(
        '%b %d, %Y %H:%M:%S'
    )

def str_to_dt(val: str) -> dt.datetime:
    return pytz.timezone(TIMEZONE).localize(
        dt.datetime.strptime(val, '%Y-%m-%d %H:%M:%S.%f')
    )
