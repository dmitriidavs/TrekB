from pydantic import ValidationError

from includes.validators import *


def validate_env_vars(env_vars: dict) -> dict:
    try:
        env_vars = EnvVars.parse_obj(env_vars)
        return env_vars.dict()
    except ValidationError as err:
        raise TypeError(err.json())


# def validate_ticker_symbol(text: str) -> bool:
#
