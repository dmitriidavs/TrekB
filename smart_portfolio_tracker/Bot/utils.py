import datetime as dt

from sqlite3 import Error as Sqlite3Error

from includes.queries.user_db_queries import *
from includes.DBMSconnection import DBMSCreateConnection


async def user_has_portfolio(user_id: str) -> bool:
    return False
