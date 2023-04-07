from typing import Union

from aioredis import Redis


class Cache(Redis):
    """Redis based cache"""

    def __init__(self, host: str, port: int, cache_ttl: int):
        super().__init__(host=host,
                         port=port)
        self.cache_ttl = cache_ttl

    async def set_data(self, key: str, value: Union[int, float, str]) -> None:
        """set"""
        await self.set(name=key, value=value, ex=self.cache_ttl)

    async def get_data(self, key: str) -> Union[int, float, str]:
        """get"""
        return await self.get(name=key)
