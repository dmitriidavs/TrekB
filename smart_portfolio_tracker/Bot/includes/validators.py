from aiogram.bot.api import check_token
from aiogram.utils.exceptions import ValidationError as AioValidErr
from pydantic import BaseModel, validator

# TODO: validation not async :(


class EnvVarsValidTypes:
    implemented_arch_types = ['Lite']
    implemented_fsm_storage_types = ['memory', 'redis']


class EnvVars(EnvVarsValidTypes, BaseModel):
    bot_arch_type: str
    bot_address: str
    bot_fsm_storage_type: str
    bot_api_token: str
    users_db_conn: str
    util_db_conn: str
    util_db_host: str
    util_db_port: int
    util_db_answers_db: int
    util_db_fsm_db: int

    @classmethod
    @validator('bot_arch_type')
    def arch_type_is_supported(cls, val: str) -> str:
        """Validate that given architecture type is supported"""

        if val not in super().implemented_arch_types:
            raise NotImplementedError(f'Error in BOT_ARCH_TYPE! Supported types: {super().implemented_arch_types}')
        else:
            return val

    @classmethod
    @validator('bot_fsm_storage_type')
    def bot_storage_is_supported(cls, val: str) -> str:
        """Validate that given storage type is supported"""

        if val not in super().implemented_fsm_storage_types:
            raise NotImplementedError(f'Error in BOT_FSM_STORAGE_TYPE! '
                                      f'Supported types: {super().implemented_fsm_storage_types}')
        else:
            return val

    @classmethod
    @validator('bot_api_token')
    def api_token_is_active(cls, val: str) -> str:
        """Validate that tg api token is active"""

        try:
            check_token(val)
            return val
        except AioValidErr:
            raise AioValidErr('Error in BOT_API_TOKEN! Invalid token.')

    # TODO: add redis conn validation
