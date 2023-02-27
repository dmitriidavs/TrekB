from sqlite3 import Error as Sqlite3Error

from creds import USERS_DB_CONN
from includes.queries.user_db_queries import *
from includes.DBMSconnection import DBMSCreateConnection


# TODO: add loggers

async def user_has_portfolio(user_id: str) -> bool:
    """Check if user has already got a portfolio running"""

    with DBMSCreateConnection(USERS_DB_CONN) as conn:
        try:
            response = conn.session.execute(
                SQL_USER_HAS_PORTFOLIO.format(user_id=user_id)
            ).fetchone()[0]
        except (Exception, Sqlite3Error) as error:
            raise error
        finally:
            conn.session.close()

        return response


# TODO?: add upsert
async def save_user_info(user_id: str, user_first_name: str, user_last_name: str,
                         user_username: str, user_language_code: str,
                         user_is_premium: bool) -> None:
    """Save user info at first contact"""

    queries = (
        SQL_ADD_NEW_USER.format(user_id=user_id),
        SQL_ADD_NEW_USER_INFO.format(
            user_id=user_id, user_first_name=user_first_name, user_last_name=user_last_name,
            user_username=user_username, user_language_code=user_language_code, user_is_premium=user_is_premium
        )
    )

    with DBMSCreateConnection(USERS_DB_CONN) as conn:
        try:
            for query in queries:
                conn.session.execute(query)
            conn.session.commit()
        except (Exception, Sqlite3Error) as error:
            raise error
        finally:
            conn.session.close()
