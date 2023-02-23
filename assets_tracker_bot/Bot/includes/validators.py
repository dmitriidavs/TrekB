from aiogram.bot.api import check_token
from aiogram.utils.exceptions import ValidationError as AioValidErr
from pydantic import (
    BaseModel,
    ValidationError,
    validator
)


class EnvVarsTypes:
    supported_arch_types = ['VM', 'Cloud', 'Lite']
    supported_fsm_storage_types = ['memory', 'db']


class EnvVars(EnvVarsTypes, BaseModel):
    bot_arch_type: str
    bot_address: str
    bot_fsm_storage_type: str
    bot_api_token: str
    user_db_conn: str

    @validator('bot_arch_type')
    def arch_type_is_supported(cls, val: str) -> str:
        if val not in super().supported_arch_types:
            raise ValueError(f'Error in BOT_ARCH_TYPE! Supported types: {super().supported_arch_types}')
        else:
            return val

    @validator('bot_fsm_storage_type')
    def bot_storage_is_supported(cls, val: str) -> str:
        if val not in super().supported_fsm_storage_types:
            raise ValueError(f'Error in BOT_FSM_STORAGE_TYPE! Supported types: {super().supported_fsm_storage_types}')
        else:
            return val

    @validator('bot_api_token')
    def api_token_is_active(cls, val: str) -> str:
        try:
            check_token(val)
            return val
        except AioValidErr:
            raise AioValidErr('Error in BOT_API_TOKEN! Invalid token.')


def validate_env_vars(env_vars: dict) -> dict:
    try:
        env_vars = EnvVars.parse_obj(env_vars)
        return env_vars.dict()
    except ValidationError as err:
        raise TypeError(err.json())
