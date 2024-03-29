from ..creds import TIMEZONE

SQL_CREATE_SCHEMA_USERS = """
CREATE SCHEMA IF NOT EXISTS users;
"""

SQL_CREATE_TABLE_ASSETS = """
CREATE TABLE IF NOT EXISTS users.assets (
    asset_id int2 PRIMARY KEY,
    ticker_symbol varchar(10) NOT NULL,
    name varchar(30) NOT NULL
);
"""

SQL_CREATE_TABLE_USERS = """
CREATE TABLE IF NOT EXISTS users.users (
    user_id int8 PRIMARY KEY,
    first_name varchar NOT NULL,
    last_name varchar NULL,
    username varchar NULL,
    language_code varchar(2) NULL,
    is_premium bool NOT NULL,
    has_portfolio bool DEFAULT FALSE,
    registration_date timestamp DEFAULT NOW(),
    update_date timestamp DEFAULT NOW()
);
"""

SQL_CREATE_TABLE_PORTFOLIO = f"""
CREATE TABLE IF NOT EXISTS users.portfolio (
    record_id serial PRIMARY KEY,
    user_id int8 NOT NULL,
    asset_id int2 NOT NULL,
    quantity float NOT NULL,
    added_at timestamp DEFAULT TIMEZONE('{TIMEZONE}', NOW()),
    FOREIGN KEY(user_id) REFERENCES users.users(user_id),
    FOREIGN KEY(asset_id) REFERENCES users.assets(asset_id)
);
"""

SQL_INSERT_DEFAULT_ASSETS = """
INSERT INTO users.assets VALUES
    (0, 'BTC', 'Bitcoin'),
    (1, 'ETH', 'Ethereum'),
    (2, 'BNB', 'BNB'),
    (3, 'XRP', 'Ripple'),
    (4, 'ADA', 'Cardano'),
    (5, 'LTC', 'Litecoin')
ON CONFLICT (asset_id) DO NOTHING;
"""