from sqlite3 import Error as UsersDBError

from .queries_user import *
from .DBMSconnection import DBMSCreateConnection
from ..creds import USERS_DB_CONN
from ..cache import cache


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
