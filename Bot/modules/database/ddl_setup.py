from asyncpg.exceptions import PostgresError as UsersDBError

from . import DBMSCreateConnection
from .queries_ddl import *
from ..creds import USERS_DB_CONN


async def setup_users_ddl():
    """Run DDL commands on bot startup"""

    ddl_queries = (
        SQL_CREATE_SCHEMA_USERS,
        SQL_CREATE_TABLE_ASSETS,
        SQL_CREATE_TABLE_USERS,
        SQL_CREATE_TABLE_PORTFOLIO,
        SQL_INSERT_DEFAULT_ASSETS
    )

    async with DBMSCreateConnection(USERS_DB_CONN) as conn:
        try:
            for query in ddl_queries:
                await conn.session.execute(query)
            await conn.session.commit()
        except UsersDBError as error:
            raise error
        finally:
            await conn.session.close()
