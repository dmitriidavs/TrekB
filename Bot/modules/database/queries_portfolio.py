SQL_ASSET_IS_SUPPORTED = """
SELECT EXISTS (
    SELECT 1 FROM users.assets
    WHERE ticker_symbol = :ticker
);
"""

SQL_ADD_ASSET_TO_PORTFOLIO = """
INSERT INTO users.portfolio (
    user_id,
    asset_id,
    quantity
) VALUES (
    :user_id,
    (
        SELECT
            asset_id
        FROM users.assets
        WHERE ticker_symbol = :asset_name
    ),
    :asset_quantity
);
"""

SQL_DELETE_PORTFOLIO = """
WITH deleted AS (
    DELETE FROM users.portfolio
    WHERE user_id = :user_id
    RETURNING record_id
)
SELECT COUNT(*) FROM deleted;
"""

SQL_SELECT_ASSETS_OUTER = """
SELECT
    p.asset_id,
    a.ticker_symbol,
    SUM(quantity)
FROM users.portfolio AS p
INNER JOIN users.assets AS a
    ON a.asset_id = p.asset_id
WHERE user_id = :user_id
GROUP BY user_id, p.asset_id, a.ticker_symbol;
"""

SQL_SELECT_ASSETS_INNER = """
SELECT
    p.record_id,
    p.asset_id,
    ticker_symbol,
    quantity,
    SUBSTRING(to_char(added_at, 'YYYY-MM-DD HH24:MI:SS.US TZ'), 1, 23) AS added_at
FROM users.portfolio AS p
INNER JOIN users.assets AS a
    ON a.asset_id = p.asset_id
WHERE user_id = :user_id AND p.asset_id = :asset_id
ORDER BY added_at DESC;
"""

SQL_UPDATE_ASSET_RECORD = """
UPDATE users.portfolio
SET {col} = :val
WHERE record_id = :record_id;
"""

SQL_DELETE_ASSET = """
DELETE FROM users.portfolio
WHERE user_id = :user_id AND asset_id = :asset_id;
"""

SQL_DELETE_RECORD = """
DELETE FROM users.portfolio
WHERE record_id = :record_id;
"""

SQL_SELECT_REMAINING = """
SELECT COUNT(*) FROM users.portfolio
WHERE user_id = :user_id
"""