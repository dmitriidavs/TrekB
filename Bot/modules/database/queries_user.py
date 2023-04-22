SQL_USER_EXISTS = """
SELECT EXISTS (
    SELECT 1 FROM users.users
    WHERE user_id = :user_id
);
"""

SQL_USER_HAS_PORTFOLIO = """
SELECT
    has_portfolio
FROM users.users
WHERE user_id = :user_id;
"""

SQL_ADD_NEW_USER = """
INSERT INTO users.users (
    user_id, first_name, last_name,
    username, language_code, is_premium
) VALUES (
    :user_id, :user_first_name, :user_last_name,
    :user_username, :user_language_code, :user_is_premium
);
"""

SQL_UPDATE_USER_HAS_PORTFOLIO_FLAG = """
UPDATE users.users
SET has_portfolio = :has_portfolio
WHERE user_id = :user_id;
"""
