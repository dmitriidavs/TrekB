import datetime as dt
from decimal import Decimal


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
    return dt.datetime.strptime(val, '%Y-%m-%d %H:%M:%S.%f %z').strftime('%b %d, %Y %H:%M:%S')
