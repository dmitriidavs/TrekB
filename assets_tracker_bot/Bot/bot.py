from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage


class ATCoreBot:
    """Core class for bot creation"""

    fsm_basic_storage: str = 'memory'

    def __init__(self,
                 arch_type: str,
                 api_key: str,
                 storage_type: str = fsm_basic_storage) -> None:
        """Param desc mb?"""

        self.arch_type = arch_type
        self.api_key = api_key
        self.storage_type = storage_type
        self.bot = None
        self.dispatcher = None
        self.set_bot()
        self.set_dispatcher()

    def set_bot(self) -> None:
        self.bot = Bot(token=self.api_key)

    def set_dispatcher(self) -> None:
        if self.storage_type == self.__class__.fsm_basic_storage:
            self.dispatcher = Dispatcher(self.bot, storage=MemoryStorage())
        else:
            # TODO: migrate to db type of storage
            pass
