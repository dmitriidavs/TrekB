import datetime as dt
import pytz

from sqlalchemy import text
from asyncpg.exceptions import PostgresError as UsersDBError

from .queries_portfolio import *
from .queries_user import SQL_UPDATE_USER_HAS_PORTFOLIO_FLAG
from . import DBMSCreateConnection
from ..creds import TIMEZONE, USERS_DB_CONN
from .. import cache


async def ticker_symbol_is_valid(ticker: str) -> bool:
    """Check if ticker symbol exists in DB"""

    # TODO: add caching in MAIN v.
    async with DBMSCreateConnection(USERS_DB_CONN) as conn:
        try:
            return (await conn.session.execute(text(SQL_ASSET_IS_SUPPORTED),
                                               {'ticker': ticker})).fetchone()[0]
        except UsersDBError as error:
            raise error
        finally:
            await conn.session.close()


async def add_asset_to_portfolio(user_id: int, asset_name: str, asset_quantity: str) -> bool:
    """
    Add new entry to user's portfolio
    ---------------------------------
    returns T/F if user added asset
    for the first time to show menu
    """

    async with DBMSCreateConnection(USERS_DB_CONN) as conn:
        try:
            # add new asset
            await conn.session.execute(text(SQL_ADD_ASSET_TO_PORTFOLIO),
                                       {'user_id': user_id,
                                        'asset_name': asset_name,
                                        'asset_quantity': asset_quantity,
                                        'added_at': dt.datetime.now(
                                            pytz.timezone(TIMEZONE)
                                        ).strftime('%Y-%m-%d %H:%M:%S')})
            await conn.session.commit()
        except UsersDBError as error:
            raise error
        else:
            # check cache if user adds asset for the first time
            c_response = await cache.get_data(key=f'user_has_portfolio:{user_id}')
            if c_response is None or int(c_response) == 0:
                try:
                    # update has_portfolio flag in users DB
                    await conn.session.execute(text(SQL_UPDATE_USER_HAS_PORTFOLIO_FLAG),
                                               {'user_id': user_id,
                                                'has_portfolio': True})
                    await conn.session.commit()
                except UsersDBError as error:
                    raise error
                else:
                    # update user_has_portfolio key
                    await cache.set_data(key=f'user_has_portfolio:{user_id}',
                                         value=1)
                    return True
            else:
                return False
        finally:
            await conn.session.close()


async def delete_portfolio(user_id: int) -> int:
    """Delete user's portfolio & update has_portfolio flags"""

    async with DBMSCreateConnection(USERS_DB_CONN) as conn:
        try:
            # delete portfolio returning number of deleted records
            response = (await conn.session.execute(text(SQL_DELETE_PORTFOLIO),
                                                   {'user_id': user_id})).fetchone()[0]
        except UsersDBError as error:
            raise error
        else:
            try:
                # update has_portfolio = False in users DB
                await conn.session.execute(text(SQL_UPDATE_USER_HAS_PORTFOLIO_FLAG),
                                           {'user_id': user_id,
                                            'has_portfolio': False})
                await conn.session.commit()
            except UsersDBError as error:
                raise error
            else:
                # update user_has_portfolio key
                await cache.set_data(key=f'user_has_portfolio:{user_id}',
                                     value=0)
                return response
        finally:
            await conn.session.close()


async def delete_asset_from_portfolio(user_id: int, asset_id: int) -> None:
    """Delete user's asset data"""

    async with DBMSCreateConnection(USERS_DB_CONN) as conn:
        try:
            await conn.session.execute(text(SQL_DELETE_ASSET),
                                       {'user_id': user_id,
                                        'asset_id': asset_id})
            await conn.session.commit()
        except UsersDBError as error:
            raise error
        else:
            # if last asset -> update has_portfolio = False in users DB
            pass
        finally:
            await conn.session.close()


async def delete_record_from_portfolio(user_id: int, asset_id: int, added_at: str) -> None:
    """Delete user's record data"""

    async with DBMSCreateConnection(USERS_DB_CONN) as conn:
        try:
            await conn.session.execute(text(SQL_DELETE_RECORD),
                                       {'user_id': user_id,
                                        'asset_id': asset_id,
                                        'added_at': added_at})
            await conn.session.commit()
        except UsersDBError as error:
            raise error
        finally:
            await conn.session.close()


async def get_assets_outer(user_id: int) -> list[tuple[int, str, float]]:
    """Get all user's assets: sum of each record"""

    async with DBMSCreateConnection(USERS_DB_CONN) as conn:
        try:
            return (await conn.session.execute(text(SQL_SELECT_ASSETS_OUTER),
                                               {'user_id': user_id})).fetchall()
        except UsersDBError as error:
            raise error
        finally:
            await conn.session.close()


async def get_assets_inner(user_id: int, asset_id: int) -> list[tuple[int, float, str]]:
    """Get user's asset activity history info"""

    async with DBMSCreateConnection(USERS_DB_CONN) as conn:
        try:
            return (await conn.session.execute(text(SQL_SELECT_ASSETS_INNER),
                                               {'user_id': user_id,
                                                'asset_id': asset_id})).fetchall()
        except UsersDBError as error:
            raise error
        finally:
            await conn.session.close()


async def update_asset_record_data(col: str, val: float, user_id: int, asset_id: int, added_at: str) -> None:
    """Update user's asset info"""

    async with DBMSCreateConnection(USERS_DB_CONN) as conn:
        try:
            await conn.session.execute(text(SQL_UPDATE_ASSET_RECORD.format(col=col)),
                                       {'val': val,
                                        'user_id': user_id,
                                        'asset_id': asset_id,
                                        'added_at': added_at})
            await conn.session.commit()
        except UsersDBError as error:
            raise error
        finally:
            await conn.session.close()


async def delete_asset_record(user_id: int, asset_id: int, added_at: str) -> None:
    """Delete user's asset record"""

    async with DBMSCreateConnection(USERS_DB_CONN) as conn:
        try:
            await conn.session.execute(text(SQL_DELETE_RECORD),
                                       {'user_id': user_id,
                                        'asset_id': asset_id,
                                        'added_at': added_at})
            await conn.session.commit()
        except UsersDBError as error:
            raise error
        finally:
            await conn.session.close()
