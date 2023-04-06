from typing import Union

from aioredis import Redis

from .creds import CACHE_TTL


class Cache(Redis):
    """Redis based cache"""

    async def set_data(self, key: str, value: Union[int, float, str]) -> None:
        """set"""
        await self.set(name=key, value=value, ex=CACHE_TTL)

    async def get_data(self, key: str) -> Union[int, float, str]:
        """get"""
        return await self.get(name=key)
