"""
TrekB | Smart Portfolio Tracker
:copyright: (c) 2023 by Dmitrii Davletshin (@dmitriidavs)
:license: BSD-3-Clause, see LICENSE for more details
"""

SQL_USER_HAS_PORTFOLIO = """
SELECT EXISTS (
    SELECT 1 FROM users
    WHERE user_id = {user_id}
);
"""

SQL_ADD_NEW_USER = """
INSERT INTO users (
    user_id
)
VALUES (
    {user_id}
);
"""

SQL_ADD_NEW_USER_INFO = """
INSERT INTO users_info (
    user_id, first_name, last_name,
    username, language_code, is_premium
) VALUES (
    {user_id}, '{user_first_name}', '{user_last_name}',
    '{user_username}', '{user_language_code}', {user_is_premium}
);
"""
