import os

from validation import validate_env_vars


env_vars = {
    'bot_arch_type': os.environ.get('BOT_ARCH_TYPE'),
    'bot_address': os.environ.get('BOT_ADDRESS'),
    'bot_fsm_storage_type': os.environ.get('BOT_FSM_STORAGE_TYPE'),
    'bot_api_token': os.environ.get('BOT_API_TOKEN'),
    'users_db_conn': os.environ.get('USERS_DB_CONN'),
    'util_db_conn': os.environ.get('USERS_DB_CONN'),
    'util_db_host': os.environ.get('UTIL_DB_HOST'),
    'util_db_port': os.environ.get('UTIL_DB_PORT'),
    'util_db_name': os.environ.get('UTIL_DB_NAME')
}

# verify correctness of environment variables
env_vars = validate_env_vars(env_vars)
# create variables from env_vars keys in upper case
for key, val in env_vars.items():
    exec(key.upper() + '=val')
