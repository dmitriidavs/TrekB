from sqlite3 import Error as UsersDBError

from .queries_portfolio import *
from .queries_user import SQL_UPDATE_USER_HAS_PORTFOLIO_FLAG
from . import DBMSCreateConnection
from ..creds import USERS_DB_CONN
from ..cache import cache


async def add_asset_to_portfolio(user_id: int, asset_name: str, asset_quantity: str) -> None:
    """Add new entry to user's portfolio"""

    async with DBMSCreateConnection(USERS_DB_CONN) as conn:
        try:
            # add new asset
            await conn.session.execute(SQL_ADD_ASSET_TO_PORTFOLIO.format(user_id=user_id,
                                                                         asset_name=asset_name,
                                                                         asset_quantity=asset_quantity))
            await conn.session.commit()
        except UsersDBError as error:
            raise error
        else:
            # check cache if user adds asset for the first time
            c_response = await cache.get(name='user_has_portfolio:' + str(user_id))
            if c_response is None or int(c_response) == 0:
                try:
                    # update has_portfolio flag in users
                    await conn.session.execute(SQL_UPDATE_USER_HAS_PORTFOLIO_FLAG.format(user_id=user_id,
                                                                                         has_portfolio=True))
                    await conn.session.commit()
                except UsersDBError as error:
                    raise error
                else:
                    # update user_has_portfolio key
                    await cache.set(name='user_has_portfolio:' + str(user_id),
                                    value=1)
        finally:
            await conn.session.close()


async def delete_portfolio(user_id: int) -> int:
    """Delete user's portfolio & update has_portfolio flags"""

    async with DBMSCreateConnection(USERS_DB_CONN) as conn:
        try:
            # delete portfolio returning number of deleted records
            await conn.session.execute(SQL_DELETE_PORTFOLIO.format(user_id=user_id))
            # TODO: to be changed in pg
            response = await conn.session.execute("""SELECT CHANGES()""")
            response = response.fetchone()[0]
        except UsersDBError as error:
            raise error
        else:
            try:
                # update has_portfolio in users
                await conn.session.execute(SQL_UPDATE_USER_HAS_PORTFOLIO_FLAG.format(user_id=user_id,
                                                                                     has_portfolio=False))
                await conn.session.commit()
            except UsersDBError as error:
                raise error
            else:
                # update user_has_portfolio key
                await cache.set(name='user_has_portfolio:' + str(user_id),
                                value=0)
        finally:
            await conn.session.close()

    return response


async def get_assets_outer(user_id: int) -> list[tuple[int, str, float]]:
    """Get all user's assets: sum of each record"""

    async with DBMSCreateConnection(USERS_DB_CONN) as conn:
        try:
            response = await conn.session.execute(SQL_SELECT_ASSETS_OUTER.format(user_id=user_id))
            response = response.fetchall()
            return response
        except UsersDBError as error:
            raise error
        finally:
            await conn.session.close()


async def get_assets_inner(user_id: int, asset_id: int) -> list[tuple[int, float, str]]:
    """Get user's asset activity history info"""

    async with DBMSCreateConnection(USERS_DB_CONN) as conn:
        try:
            response = await conn.session.execute(SQL_SELECT_ASSETS_INNER.format(user_id=user_id,
                                                                                 asset_id=asset_id))
            response = response.fetchall()
            return response
        except UsersDBError as error:
            raise error
        finally:
            await conn.session.close()


async def cache_set_asset_editing_data(data: dict) -> None:
    await cache.hset(name='editing_data:' + str(data["user_id"]),
                     mapping=data)


async def cache_get_asset_editing_data(user_id: int) -> dict:
    return await cache.hgetall(name='editing_data:' + str(user_id))


async def cache_del_asset_editing_data(user_id: int) -> None:
    await cache.delete('editing_data:' + str(user_id))


async def update_asset_record_data(col: str, val: float, user_id: int, asset_id: int, added_at: str) -> None:
    """Update user's asset info"""

    async with DBMSCreateConnection(USERS_DB_CONN) as conn:
        try:
            await conn.session.execute(SQL_UPDATE_ASSET_RECORD.format(col=col,
                                                                      val=val,
                                                                      user_id=user_id,
                                                                      asset_id=asset_id,
                                                                      added_at=added_at))
            await conn.session.commit()
        except UsersDBError as error:
            raise error
        finally:
            await conn.session.close()


# # TODO:
# async def delete_asset_record(col: str, user_id: int, asset_id: int) -> str:
#     """Get user's asset info"""
#
#     async with DBMSCreateConnection(USERS_DB_CONN) as conn:
#         try:
#             response = await conn.session.execute(SQL_SELECT_ASSETS_INNER.format(user_id=user_id,
#                                                                                  asset_id=asset_id))
#             response = response.fetchall()
#             return response
#         except UsersDBError as error:
#             raise error
#         finally:
#             await conn.session.close()
