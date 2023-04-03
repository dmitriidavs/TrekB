from aioredis import Redis

from .creds import BROKER_HOST, BROKER_PORT
from .validation.utils import gen_pointer


class Broker(Redis):
    """
    Redis message broker
    set_data, get_data, del_data: user has multiple choice (e.g. callback buttons)
    else: user in some FSM state
    """

    async def set_data(self, user_id: int, data: dict) -> None:
        pointer = gen_pointer()
        await self.hset(name=f'{user_id}:{pointer}',
                        mapping=data.update({'pointer': pointer}))

    async def get_data(self, user_id: int, pointer: str) -> dict:
        return await self.hgetall(name=f'{user_id}:{pointer}')

    async def del_data(self, user_id: int, pointer: str) -> None:
        await self.delete(f'{user_id}:{pointer}')

    async def set_asset_editing_data(self, data: dict) -> None:
        await self.hset(name=f'asset_editing_data:{data["user_id"]}',
                        mapping=data)

    async def get_asset_editing_data(self, user_id: int) -> dict:
        return await self.hgetall(name=f'asset_editing_data:{user_id}')

    async def del_asset_editing_data(self, user_id: int) -> None:
        await self.delete(f'asset_editing_data:{user_id}')


broker = Broker(host=BROKER_HOST,
                port=BROKER_PORT,
                decode_responses=True)
