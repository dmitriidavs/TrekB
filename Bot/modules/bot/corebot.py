from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2

from ..creds import FSM_TTL


class CoreBot:
    """Core class for bot creation"""

    def __init__(self,
                 api_token: str, storage_type: str,
                 cache_host: str, cache_port: int):
        self.storage_type = storage_type
        self.api_token = api_token
        self.cache_host = cache_host
        self.cache_port = cache_port
        self.storage = None
        self.bot = self.set_bot()
        self.dispatcher = self.set_dispatcher()

    def set_bot(self) -> Bot:
        return Bot(token=self.api_token)

    def set_dispatcher(self) -> Dispatcher:
        if self.storage_type == 'memory':
            self.storage = MemoryStorage()
        elif self.storage_type == 'redis':
            self.storage = RedisStorage2(host=self.cache_host,
                                         port=self.cache_port,
                                         state_ttl=FSM_TTL)

        return Dispatcher(self.bot, storage=self.storage)
