## Bot Organization:

    └── modules                 <- python packages
    |   └── bot                     <- bot package
    |   |   ├── __init__.py             <- creates bot & dispatcher depending on architecture
    |   |   ├── bot.py                  <- bot classes for different architectures
    |   |   └── bot_ctx.py              <- bot context
    |   └── callbacks               <- callbacks package
    |   |   ├── __init__.py             <- registrates callbacks
    |   |   └── callbacks_portfolio.py  <- functions for portfolio callback processing
    |   └── database                <- callbacks package
    |   |   ├── __init__.py             <- creates async DB connection context manager
    |   |   ├── create_db.sql           <- SQL DDL queries, activated on bot start
    |   |   ├── logic_portfolio.py      <- functions for portfolio dialogue DB logic processing
    |   |   ├── logic_user.py           <- functions for user dialogue DB logic processing
    |   |   ├── queries_portfolio.py    <- portfolio SQL queries for users DB
    |   |   └── queries_user.py         <- user SQL queries for users DB
    |   └── handlers                <- handlers package
    |   |   ├── __init__.py             <- registrates handlers
    |   |   ├── fsm.py                  <- finite state machines for dialogue state memorization
    |   |   ├── handlers_portfolio.py   <- functions for portfolio commands processing
    |   |   └── handlers_user.py        <- functions for user commands processing
    |   └── keyboards               <- keyboards package
    |   |   ├── __init__.py             <- imports only
    |   |   ├── callback.py             <- functions for multi-level portfolio inline keyboard processing
    |   |   ├── inline.py               <- functions for inline buttons creation
    |   |   └── reply.py                <- functions for reply buttons creation
    |   └── log                     <- log package
    |   |   ├── __init__.py             <- creates logging configs
    |   |   └── loggers.py              <- logging decorators
    |   └── validation              <- validation package
    |   |   ├── __init__.py             <- creates validation functions
    |   |   └── validators.py           <- pydantic validator classes
    |   ├── __init__.py             <- imports only
    |   ├── cache.py                <- Redis client for caching
    |   └── creds.py                <- environment variables getter & setter
    ├── .venv_example.bat       <- example of VM variables to run locally
    ├── README.md               <- Bot README
    ├── app.py                  <- entrypoint
    └── requirements.txt        <- required python packages
