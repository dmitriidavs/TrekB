from typing import Union

from aioredis import Redis

from .validation.utils import gen_pointer


class Broker(Redis):
    """
    Redis based message broker
    --------------------------
    set_data, get_data, del_data, multi_exec_data:
        user has multiple choice (e.g.: callback buttons)
    else:
        user in some FSM state
    """

    async def set_data(self, user_id: int, data: Union[dict, tuple[tuple]]) -> Union[dict, tuple]:
        """hset or multi/exec hset"""

        if isinstance(data, tuple):
            data_dict = dict((data[i], data[i + 1]) for i in range(0, len(data), 2))
            # data = [{}]
            async with self.pipeline(transaction=True) as pipe:
                for b_data, b_name in zip(data[0], data[1]):
                    pointer = gen_pointer()

                    b_data["pointer"] = pointer
                    await pipe.hset(name=f'{user_id}:{pointer}',
                                    mapping=b_data)
                    data.append(b_data)
                # execute transaction
                await pipe.execute()
                return tuple(data)
        else:
            pointer = gen_pointer()
            data["pointer"] = pointer
            await self.hset(name=f'{user_id}:{pointer}',
                            mapping=data)
            return data

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
