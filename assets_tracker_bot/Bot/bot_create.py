from bot import LiteBot
from creds import BOT_API_TOKEN, BOT_ARCH_TYPE, USERS_DB_CONN, BOT_FSM_STORAGE_TYPE


# TODO: create bot class depending on ARCH_TYPE
BaseBot = LiteBot(api_token=BOT_API_TOKEN,
                  arch_type=BOT_ARCH_TYPE,
                  users_db_conn=USERS_DB_CONN,
                  storage_type=BOT_FSM_STORAGE_TYPE)
bot = BaseBot.bot
dispatcher = BaseBot.dispatcher
