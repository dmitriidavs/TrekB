CREATE TABLE IF NOT EXISTS assets(
    asset_id int2 PRIMARY KEY,
    ticker_symbol varchar(10) UNIQUE,
    name varchar(30) UNIQUE
);

CREATE TABLE IF NOT EXISTS users(
    user_id integer PRIMARY KEY,
    join_date datetime NOT NULL
);

CREATE TABLE IF NOT EXISTS portfolio(
    user_id integer NOT NULL,
    asset_id int2 NOT NULL,
    quantity float NOT NULL,
    created_at datetime NOT NULL,
    PRIMARY KEY(user_id, asset_id),
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

--PRAGMA foreign_keys = ON; as an additional command in Dockerfile