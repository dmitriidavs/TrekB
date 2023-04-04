from typing import Union

from aioredis import Redis

from .validation.utils import gen_pointer


# TODO: implement check for duplicate data (prefix?)
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

        pointer = await gen_pointer()
        data["pointer"] = pointer
        await self.hset(name=f'{user_id}:{pointer}',
                        mapping=data)
        return data

    async def multi_exec_hset(self, user_id: int, data: tuple[tuple]) -> tuple[dict]:
        """multi/exec hset"""

        # start transaction
        async with self.pipeline(transaction=True) as pipe:
            result = []
            for b_data in data[0]:
                # create dict from data & attributes tuples
                res_dict = {key: val for key, val in zip(data[1], b_data)}
                pointer = await gen_pointer()
                res_dict["pointer"] = pointer
                result.append(res_dict)
                # add hset command to the pipe
                await pipe.hset(name=f'{user_id}:{pointer}',
                                mapping=res_dict)
            # execute transaction
            await pipe.execute()
            # return resulting dictionaries
            return tuple(result)

    async def get_data(self, user_id: int, pointer: str) -> dict:
        """hgetall"""

        return await self.hgetall(name=f'{user_id}:{pointer}')

    async def del_data(self, user_id: int, pointer: str) -> None:
        """del"""

        await self.delete(f'{user_id}:{pointer}')

    async def set_asset_editing_data(self, data: dict) -> None:
        await self.hset(name=f'asset_editing_data:{data["user_id"]}',
                        mapping=data)

    async def get_asset_editing_data(self, user_id: int) -> dict:
        return await self.hgetall(name=f'asset_editing_data:{user_id}')

    async def del_asset_editing_data(self, user_id: int) -> None:
        await self.delete(f'asset_editing_data:{user_id}')
