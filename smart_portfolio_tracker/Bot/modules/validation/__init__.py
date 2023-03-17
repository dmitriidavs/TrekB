__all__ = ['validators', 'formatters',
           'validate_env_vars', 'validate_asset_name',
           'validate_text_is_float', 'validate_float_is_not_int']

from pydantic import ValidationError

from .validators import EnvVars


def validate_env_vars(env_vars: dict) -> dict:
    try:
        env_vars = EnvVars.parse_obj(env_vars)
        return env_vars.dict()
    except ValidationError as err:
        raise TypeError(err.json())


async def validate_asset_name(ticker: str) -> bool:
    """Check if ticker symbol is valid"""

    # TODO: add caching
    # TODO: add real validation xD
    if ticker == 'err':     # test
        return False
    else:
        return True


async def validate_text_is_float(text: str) -> bool:
    """Check if text can be converted to float"""

    try:
        float(text)
        return True
    except ValueError:
        return False
