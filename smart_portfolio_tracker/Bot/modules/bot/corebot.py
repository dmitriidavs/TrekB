from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2


class CoreBot:
    """Core class for bot creation"""

    def __init__(self,
                 api_token: str, storage_type: str,
                 util_db_host: str, util_db_port: int):
        self.storage_type = storage_type
        self.api_token = api_token
        self.util_db_host = util_db_host
        self.util_db_port = util_db_port
        self.storage = None
        self.bot = self.set_bot()
        self.dispatcher = self.set_dispatcher()

    def set_bot(self) -> Bot:
        return Bot(token=self.api_token)

    def set_dispatcher(self) -> Dispatcher:
        if self.storage_type == 'memory':
            self.storage = MemoryStorage()
        elif self.storage_type == 'redis':
            self.storage = RedisStorage2(host=self.util_db_host,
                                         port=self.util_db_port)

        return Dispatcher(self.bot, storage=self.storage)


# class LiteBot(CoreBot):
#     """Lite Bot class creator"""
#
#     def __init__(self,
#                  api_token: str, arch_type: str, users_db_conn: str, util_db_host: str,
#                  util_db_port: int, storage_type: str):
#
#         super().__init__(api_token, storage_type, util_db_host, util_db_port)
#         super().set_bot()
#         super().set_dispatcher()
#         self.arch_type = arch_type
#         self.users_db_conn = users_db_conn
#         # TODO: add connectors to db through external parent class in DBMSconnection
#         # smth like set_conn depending on bot class

