import os

from .validation import validate_env_vars


# validate environment variables
env_vars = validate_env_vars({
    'bot_arch_type': os.environ.get('BOT_ARCH_TYPE'),
    'bot_address': os.environ.get('BOT_ADDRESS'),
    'bot_fsm_storage_type': os.environ.get('BOT_FSM_STORAGE_TYPE'),
    'bot_api_token': os.environ.get('BOT_API_TOKEN'),
    'users_db_conn': os.environ.get('USERS_DB_CONN'),
    'util_db_host': os.environ.get('UTIL_DB_HOST'),
    'util_db_port': os.environ.get('UTIL_DB_PORT'),
    'log_folder_path': os.environ.get('LOG_FOLDER_PATH'),
    'log_host': os.environ.get('LOG_HOST'),
    'log_port': os.environ.get('LOG_PORT'),
})

BOT_ARCH_TYPE = env_vars['bot_arch_type']
BOT_ADDRESS = env_vars['bot_address']
BOT_FSM_STORAGE_TYPE = env_vars['bot_fsm_storage_type']
BOT_API_TOKEN = env_vars['bot_api_token']
USERS_DB_CONN = env_vars['users_db_conn']
UTIL_DB_HOST = env_vars['util_db_host']
UTIL_DB_PORT = env_vars['util_db_port']
LOG_FOLDER_PATH = env_vars['log_folder_path']
LOG_HOST = env_vars['log_host']
LOG_PORT = env_vars['log_port']
