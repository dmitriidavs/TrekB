from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

# from includes.DBMSconnection import


class ATCoreBot:
    """Core class for bot creation"""

    def __init__(self, api_token: str, storage_type: str):
        self.storage_type = storage_type
        self.api_token = api_token
        self.bot = None
        self.dispatcher = None

    def set_bot(self) -> None:
        self.bot = Bot(token=self.api_token)

    def set_dispatcher(self) -> None:
        if self.storage_type == 'memory':
            storage = MemoryStorage()
        else:
            # TODO: migrate to db type of storage (SQLite)
            storage = None

        self.dispatcher = Dispatcher(self.bot, storage=storage)


class LiteBot(ATCoreBot):
    """Lite Bot class creator"""

    def __init__(self, api_token: str, arch_type: str, users_db_conn: str, storage_type: str = 'memory'):
        super().__init__(api_token, storage_type)
        super().set_bot()
        super().set_dispatcher()
        self.arch_type = arch_type
        self.users_db_conn = users_db_conn
        # TODO: add connectors to db through external parent class in DBMSconnection
        # self.conn =

