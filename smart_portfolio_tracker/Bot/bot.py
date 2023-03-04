from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2


class CoreBot:
    """Core class for bot creation"""

    def __init__(self, api_token: str, storage_type: str,
                 util_db_host: str, util_db_port: int, util_db_fsm_db: int):
        self.storage_type = storage_type
        self.api_token = api_token
        self.util_db_host = util_db_host
        self.util_db_port = util_db_port
        self.util_db_fsm_db = util_db_fsm_db
        self.storage = None
        self.bot = None
        self.dispatcher = None

    def set_bot(self) -> None:
        self.bot = Bot(token=self.api_token)

    def set_dispatcher(self) -> None:
        if self.storage_type == 'memory':
            self.storage = MemoryStorage()
        elif self.storage_type == 'redis':
            self.storage = RedisStorage2(
                host=self.util_db_host,
                port=self.util_db_port,
                db=self.util_db_fsm_db
            )

        self.dispatcher = Dispatcher(self.bot, storage=self.storage)


class LiteBot(CoreBot):
    """Lite Bot class creator"""

    def __init__(self, api_token: str, arch_type: str, users_db_conn: str, util_db_host: str,
                 util_db_port: int, util_db_fsm_db: int, storage_type: str = 'memory'):

        super().__init__(api_token, storage_type, util_db_host, util_db_port, util_db_fsm_db)
        super().set_bot()
        super().set_dispatcher()
        self.arch_type = arch_type
        self.users_db_conn = users_db_conn
        # TODO: add connectors to db through external parent class in DBMSconnection
        # smth like set_conn depending on bot class

