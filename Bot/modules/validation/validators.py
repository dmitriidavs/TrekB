from typing import Optional
from pytz import all_timezones as pytz_timezones
from pytz.exceptions import UnknownTimeZoneError

import requests
from requests.exceptions import HTTPError, ConnectionError
from aiogram.bot.api import check_token
from aiogram.utils.exceptions import Unauthorized
from pydantic import BaseModel, validator


class EnvVarsValidTypes:
    implemented_arch_types = ('Lite', 'Prod',)
    implemented_fsm_storage_types = ('memory', 'redis',)
    implemented_log_types = ('cli', 'file', 'service',)


class EnvVars(EnvVarsValidTypes, BaseModel):
    # tz
    timezone: str

    # bot
    bot_arch_type: str
    bot_address: str
    bot_fsm_storage_type: str
    bot_api_token: str

    # users DB conn
    users_db_conn: str

    # cache
    cache_host: str
    cache_port: int

    # broker
    broker_host: str
    broker_port: int

    # ttl
    cache_ttl: int
    fsm_ttl: int
    broker_ttl: int

    # logging
    log_folder_path: str
    log_host: Optional[str]
    log_port: Optional[int]
    log_type: str

    # webhook
    webhook_url: str

    # links
    project_link: str
    supported_assets_link: str

    @validator('timezone')
    @classmethod
    def timezone_is_valid(cls, val: str) -> str:
        """Validate that given timezone exists"""

        if val not in pytz_timezones:
            raise UnknownTimeZoneError(f'Error in TIMEZONE! {val} is invalid')
        else:
            return val

    @validator('bot_arch_type')
    @classmethod
    def arch_type_is_supported(cls, val: str) -> str:
        """Validate that given architecture type is supported"""

        if val not in super().implemented_arch_types:
            raise NotImplementedError(f'Error in BOT_ARCH_TYPE! '
                                      f'Supported types: {super().implemented_arch_types}')
        else:
            return val

    @validator('bot_fsm_storage_type')
    @classmethod
    def bot_storage_type_is_supported(cls, val: str) -> str:
        """Validate that given storage type is supported"""

        if val not in super().implemented_fsm_storage_types:
            raise NotImplementedError(f'Error in BOT_FSM_STORAGE_TYPE! '
                                      f'Supported types: {super().implemented_fsm_storage_types}')
        else:
            return val

    @validator('log_type')
    @classmethod
    def log_type_is_supported(cls, val: str, values: dict) -> str:
        """Validate that given log type is supported"""

        log_host = values['log_host']
        log_port = values['log_port']

        if val not in super().implemented_log_types:
            raise NotImplementedError(f'Error in LOG_TYPE! '
                                      f'Supported types: {super().implemented_log_types}')
        elif val == 'service' and any(val is None for val in (log_host, log_port)):
            raise ValueError(f'LOG_TYPE (service) should include LOG_HOST & LOG_PORT values.')
        else:
            return val

    @validator('bot_api_token')
    @classmethod
    def api_token_is_active(cls, val: str) -> str:
        """Validate that tg api token is active"""

        if not check_token(val):
            raise Unauthorized('Error in BOT_API_TOKEN! Invalid token.')
        else:
            return val

    @validator('project_link', 'supported_assets_link')
    @classmethod
    def link_is_active(cls, val: str) -> str:
        """Validate that link is active"""

        try:
            if requests.get(val).status_code != 200:
                raise HTTPError(f'Connection to {val} is not active.')
            else:
                return val
        except ConnectionError:
            raise Exception(f'Invalid Credentials in {val}.')
