from sqlite3 import Error as UsersDBError

from creds import USERS_DB_CONN
from cache import cache
from includes.loggers.log import bench_query
from includes.queries.users_db_queries import *
from includes.DBMSconnection import DBMSCreateConnection


async def user_exists(user_id: int) -> bool:
    """
    Check if user exists in users DB
    --------------------------------
    DB queried on initial contact only, then
    cache gets set in func: save_user_info
    """

    # check cache if user exists in users DB
    c_response = await cache.get(name='user_exists:' + str(user_id))
    # if cache not set
    if c_response is None:
        async with DBMSCreateConnection(USERS_DB_CONN) as conn:
            try:
                # check users DB if user exists
                response = await conn.session.execute(
                    SQL_USER_EXISTS.format(user_id=user_id)
                )
                response = response.fetchone()[0]
                # save response in cache    # TODO: add expiry time
                await cache.set(name='user_exists:' + str(user_id),
                                value=response)
                return response
            except UsersDBError as error:
                raise error
            finally:
                await conn.session.close()
    # use cached val
    else:
        return bool(c_response)


async def user_has_portfolio(user_id: int) -> int:
    """
    Check if user has already got a portfolio
    -----------------------------------------
    Activated only on first /start, then cache key user_has_portfolio
    is updated through /add & /flushit cmds
    """

    # check cache if user has portfolio
    c_response = await cache.get(name='user_has_portfolio:' + str(user_id))
    # if cache not set
    if c_response is None:
        async with DBMSCreateConnection(USERS_DB_CONN) as conn:
            try:
                # check users DB if user has portfolio
                response = await conn.session.execute(
                    SQL_USER_HAS_PORTFOLIO.format(user_id=user_id)
                )
                response = response.fetchone()[0]
                # save answer in cache
                await cache.set(name='user_has_portfolio:' + str(user_id),
                                value=response)
                return response
            except UsersDBError as error:
                raise error
            finally:
                await conn.session.close()
    else:
        return int(c_response)


# TODO: add upsert?
async def save_user_info(user_id: int, user_first_name: str, user_last_name: str,
                         user_username: str, user_language_code: str,
                         user_is_premium: bool) -> None:
    """Save user info at first dialogue contact"""

    queries = (
        SQL_ADD_NEW_USER.format(user_id=user_id),
        SQL_ADD_NEW_USER_INFO.format(
            user_id=user_id, user_first_name=user_first_name, user_last_name=user_last_name,
            user_username=user_username, user_language_code=user_language_code, user_is_premium=user_is_premium
        )
    )

    async with DBMSCreateConnection(USERS_DB_CONN) as conn:
        try:
            for query in queries:
                await conn.session.execute(query)
            await conn.session.commit()
        except UsersDBError as error:
            raise error
        finally:
            await conn.session.close()

    # update user_exists key
    await cache.set(name='user_exists:' + str(user_id),
                    value=1)


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
