from aioredis import Redis

from .creds import BROKER_HOST, BROKER_PORT


class Broker(Redis):
    """Redis message broker"""

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
