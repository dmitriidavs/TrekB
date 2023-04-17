from aiogram import Bot, Dispatcher


class WebhookBot:
    """Class for webhook bot creation"""

    def __init__(self, api_token: str):
        self.api_token = api_token
        self.bot = self.set_bot()
        self.dispatcher = self.set_dispatcher()

    def set_bot(self) -> Bot:
        return Bot(token=self.api_token)

    def set_dispatcher(self) -> Dispatcher:
        return Dispatcher(self.bot)
