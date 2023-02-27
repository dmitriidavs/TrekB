CREATE TABLE IF NOT EXISTS assets(
    asset_id int2 PRIMARY KEY,
    ticker_symbol varchar(10) UNIQUE,
    name varchar(30) UNIQUE
);

-- TODO: convert timestamp to datetimetz in pg
CREATE TABLE IF NOT EXISTS users (
    user_id integer PRIMARY KEY,
    has_portfolio boolean DEFAULT false,
    join_date timestamp DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS users_info (
    user_id integer PRIMARY KEY,
    first_name varchar(30) NOT NULL,
    last_name varchar(30) NULL,
    username varchar(30) NULL,
    language_code varchar(2) NULL,
    is_premium boolean NULL,
    FOREIGN KEY(user_id) REFERENCES users(user_id)
);

-- move to SCD2
CREATE TABLE IF NOT EXISTS portfolio (
    user_id integer NOT NULL,
    asset_id int2 NOT NULL,
    quantity float NOT NULL,
    added_at timestamp DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(user_id, asset_id),
    FOREIGN KEY(user_id) REFERENCES users(user_id),
    FOREIGN KEY(asset_id) REFERENCES assets(asset_id)
);

-- TODO: move to API solution
INSERT OR IGNORE INTO assets VALUES
    (0, 'BTC', 'Bitcoin'),
    (1, 'ETH', 'Ethereum'),
    (2, 'BNB', 'BNB'),
    (3, 'XRP', 'Ripple'),
    (4, 'ADA', 'Cardano'),
    (5, 'MSFT', 'Microsoft'),
    (6, 'GOOGL', 'Google'),
    (7, 'GOLD', 'Gold');

-- PRAGMA foreign_keys = ON; as an additional command in Dockerfile