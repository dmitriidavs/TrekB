SQL_USER_EXISTS = """
SELECT EXISTS (
    SELECT 1 FROM users
    WHERE user_id = {user_id}
);
"""

SQL_USER_HAS_PORTFOLIO = """
SELECT
    has_portfolio
FROM users
WHERE user_id = {user_id};
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

SQL_ADD_ASSET_TO_PORTFOLIO = """
INSERT INTO portfolio (
    user_id,
    asset_id,
    quantity
) VALUES (
    {user_id},
    (
        SELECT
            asset_id
        FROM assets
        WHERE ticker_symbol = '{asset_name}'
    ),
    {asset_quantity}
);
"""

SQL_UPDATE_USER_HAS_PORTFOLIO = """
UPDATE users
SET has_portfolio = {has_portfolio}
WHERE user_id = {user_id}
"""
