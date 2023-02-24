# Bot Organization:

    ├── README.md               <- Bot README
    ├── bot_run.py              <- entrypoint
    ├── bot_create.py           <- bot creator depending on chosen config
    ├── bot.py                  <- bot objects depending on chosen architecture
    ├── handlers.py             <- handlers for user commands in Telegram UI
    ├── creds.py                <- environment variables getter and configurator
    ├── validation.py           <- functions forming the validation layer
    ├── utils.py                <- functions that process dialogue logic and DB communication
    ├── .venv_example.bat       <- virtual environment variables setter for local use
    └── includes                <- additional 
    |   ├── DBMSconnection.py           <- async DB connection context manager object
    |   ├── finite_state_machines.py    <- objects that memorize dialogue states
    |   ├── keyboards.py                <- keyboards for user to click on
    |   ├── validators.py               <- validation layer objects that
    |   └── loggers                     <- bot logging
    |   |   └── debug.py                        <- CMD bot logging
    |   └── queries                     <- DB queries
    |   |   └── user_db.py                      <- SQLite user DB queries
