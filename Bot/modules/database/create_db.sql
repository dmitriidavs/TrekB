CREATE TABLE IF NOT EXISTS assets (
    asset_id int2 PRIMARY KEY,
    ticker_symbol varchar(10) NOT NULL,
    name varchar(30) NOT NULL
);

-- TODO: convert timestamp to datetimetz in pg
CREATE TABLE IF NOT EXISTS users (
    user_id integer PRIMARY KEY,
    has_portfolio boolean DEFAULT false,
    registration_date timestamp DEFAULT CURRENT_TIMESTAMP,
    update_date timestamp DEFAULT CURRENT_TIMESTAMP     -- should track log
);

CREATE TABLE IF NOT EXISTS users_info (
    user_id integer PRIMARY KEY,
    first_name varchar(30) NOT NULL,
    last_name varchar(30) NULL,
    username varchar(30) NULL,
    language_code varchar(2) NULL,
    is_premium boolean NOT NULL,
    FOREIGN KEY(user_id) REFERENCES users(user_id)
);

-- TODO: move to SCD2
CREATE TABLE IF NOT EXISTS portfolio (
    user_id integer NOT NULL,
    asset_id int2 NOT NULL,
    quantity float NOT NULL,
    added_at timestamp DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(user_id, asset_id, added_at),
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
    (5, 'LTC', 'Litecoin')

PRAGMA foreign_keys = ON;