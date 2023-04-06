from typing import Union

from aioredis import Redis

from .validation.utils import HashDict
from .creds import BROKER_TTL


class Broker(Redis):
    """
    Redis based message broker
    --------------------------
    set_data, get_data, del_data, multi_exec_data:
        used when user has multiple choice (e.g.: callback buttons)
    else:
        used when user in some FSM state
    """

    async def set_data(self, user_id: int, data: Union[dict, tuple[tuple]]) -> Union[dict, tuple[dict]]:
        """
        data:
            1. dict -> hset
            2. tuple[tuple_of_data_tuples, tuple_of_str_attributes] -> multi/exec hset
        """

        if isinstance(data, tuple):
            return await self.multi_exec_hset(user_id, data)
        else:
            return await self.exec_hset(user_id, data)

    async def exec_hset(self, user_id: int, data: dict) -> dict:
        """hset"""

        # generate hash part of key from data dict
        pointer = await HashDict.get_dict_hash(data)
        data["pointer"] = pointer

        # check if key not in broker
        if not await self.exists_data(user_id, pointer):
            # pipe hset + set expiry time
            async with self.pipeline(transaction=True) as pipe:
                await pipe.hset(name=f'{user_id}:{pointer}',
                                mapping=data)
                await pipe.expire(name=f'{user_id}:{pointer}',
                                  time=BROKER_TTL)
                # execute transaction if any tasks exist
                await pipe.execute()

        return data

    async def multi_exec_hset(self, user_id: int, data: tuple[tuple]) -> tuple[dict]:
        """multi/exec hset"""

        result = []
        # start transaction
        async with self.pipeline(transaction=True) as pipe:
            for b_data in data[0]:
                # create dict from data & attributes tuples
                data_dict = {key: val for key, val in zip(data[1], b_data)}

                # generate hash part of key from data_dict
                pointer = await HashDict.get_dict_hash(data_dict)

                data_dict["pointer"] = pointer
                result.append(data_dict)

                # pipe hset + set expiry time if key not in broker
                if not await self.exists_data(user_id, pointer):
                    await pipe.hset(name=f'{user_id}:{pointer}',
                                    mapping=data_dict)
                    await pipe.expire(name=f'{user_id}:{pointer}',
                                      time=BROKER_TTL)

            # execute transaction if any tasks exist
            await pipe.execute()
            # return resulting dictionaries
            return tuple(result)

    async def exists_data(self, user_id: int, pointer: str) -> bool:
        """exists"""
        return await self.exists(f'{user_id}:{pointer}')

    async def get_data(self, user_id: int, pointer: str) -> dict:
        """hgetall"""
        return await self.hgetall(name=f'{user_id}:{pointer}')

    async def del_data(self, user_id: int, pointer: str) -> None:
        """del"""
        await self.delete(f'{user_id}:{pointer}')

    async def set_asset_editing_data(self, data: dict) -> None:
        # pipe hset + set expiry time
        async with self.pipeline(transaction=True) as pipe:
            await pipe.hset(name=f'asset_editing_data:{data["user_id"]}',
                            mapping=data)
            await pipe.expire(name=f'asset_editing_data:{data["user_id"]}',
                              time=BROKER_TTL)
            # execute transaction
            await pipe.execute()

    async def get_asset_editing_data(self, user_id: int) -> dict:
        # pipe hgetall + del
        async with self.pipeline(transaction=True) as pipe:
            await pipe.hgetall(name=f'asset_editing_data:{user_id}')
            await pipe.delete(f'asset_editing_data:{user_id}')
            # execute transaction
            result = await pipe.execute()
            return result[0]
