from pytz import all_timezones, exceptions
from typing import Optional

from aiogram.bot.api import check_token
from aiogram.utils.exceptions import Unauthorized
from pydantic import BaseModel, validator


class EnvVarsValidTypes:
    implemented_arch_types = ['Lite']
    implemented_fsm_storage_types = ['memory', 'redis']


class EnvVars(EnvVarsValidTypes, BaseModel):
    timezone: str
    bot_arch_type: str
    bot_address: str
    bot_fsm_storage_type: str
    bot_api_token: str
    users_db_conn: str
    cache_host: str
    cache_port: int
    broker_host: str
    broker_port: int
    cache_ttl: int
    fsm_ttl: int
    broker_ttl: int
    log_folder_path: str
    log_host: Optional[str]
    log_port: Optional[int]

    @validator('timezone')
    @classmethod
    def timezone_is_valid(cls, val: str) -> str:
        """Validate that given timezone exists"""

        if val not in all_timezones:
            raise exceptions.UnknownTimeZoneError(f'Error in TIMEZONE! {val} is invalid')
        else:
            return val

    @validator('bot_arch_type')
    @classmethod
    def arch_type_is_supported(cls, val: str) -> str:
        """Validate that given architecture type is supported"""

        if val not in super().implemented_arch_types:
            raise NotImplementedError(f'Error in BOT_ARCH_TYPE! Supported types: {super().implemented_arch_types}')
        else:
            return val

    @validator('bot_fsm_storage_type')
    @classmethod
    def bot_storage_is_supported(cls, val: str) -> str:
        """Validate that given storage type is supported"""

        if val not in super().implemented_fsm_storage_types:
            raise NotImplementedError(f'Error in BOT_FSM_STORAGE_TYPE! '
                                      f'Supported types: {super().implemented_fsm_storage_types}')
        else:
            return val

    @validator('bot_api_token')
    @classmethod
    def api_token_is_active(cls, val: str) -> str:
        """Validate that tg api token is active"""

        try:
            check_token(val)
            return val
        except Unauthorized:
            raise Unauthorized('Error in BOT_API_TOKEN! Invalid token.')
