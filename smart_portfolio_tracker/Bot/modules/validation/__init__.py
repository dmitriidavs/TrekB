__all__ = ['formatters', 'validators',
           'validate_env_vars', 'validate_text_is_positive_float', 'validate_date_format']

import datetime as dt

from pydantic import ValidationError

from .validators import EnvVars


def validate_env_vars(env_vars: dict) -> dict:
    try:
        env_vars = EnvVars.parse_obj(env_vars)
        return env_vars.dict()
    except ValidationError as err:
        raise TypeError(err.json())


async def validate_text_is_positive_float(text: str) -> bool:
    """Check if text can be converted to float"""

    try:
        if float(text) > 0:
            return True
    except ValueError:
        return False


async def validate_date_format(text: str) -> bool:
    """Check if date follows suggested format"""

    try:
        dt.datetime.strptime(text, '%Y-%m-%d %H:%M:%S')
        return True
    except ValueError:
        return False
