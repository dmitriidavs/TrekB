from bot import LiteBot
from creds import BOT_API_TOKEN, BOT_ARCH_TYPE, USER_DB_CONN, BOT_FSM_STORAGE_TYPE


# TODO: create bot class depending on ARCH_TYPE
BaseBot = LiteBot(api_token=BOT_API_TOKEN,
                  arch_type=BOT_ARCH_TYPE,
                  user_db_conn=USER_DB_CONN,
                  storage_type=BOT_FSM_STORAGE_TYPE)
bot = BaseBot.bot
dispatcher = BaseBot.dispatcher
