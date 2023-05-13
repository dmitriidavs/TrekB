## Bot Organization:

    └── modules                 <- python packages
    |   └── bot                     <- bot package
    |   |   ├── __init__.py             <- creates bot & dispatcher clients
    |   |   ├── corebot.py              <- bot classes for different architectures
    |   |   └── bot_ctx.py              <- bot context
    |   └── database                <- callbacks package
    |   |   ├── __init__.py             <- creates async DB connection context manager
    |   |   ├── ddl.sql                 <- SQL DDL queries for users DB
    |   |   ├── logic_portfolio.py      <- functions for portfolio dialogue DB logic processing
    |   |   ├── logic_user.py           <- functions for user dialogue DB logic processing
    |   |   ├── queries_portfolio.py    <- portfolio SQL queries for users DB
    |   |   └── queries_user.py         <- user SQL queries for users DB
    |   └── handlers                <- handlers package
    |   |   ├── __init__.py             <- registrates handlers
    |   |   ├── fsm.py                  <- finite state machines for dialogue state memorization
    |   |   ├── handlers_portfolio.py   <- functions for portfolio commands processing
    |   |   └── handlers_user.py        <- functions for general commands processing
    |   └── keyboards               <- keyboards package
    |   |   ├── __init__.py             <- imports only
    |   |   ├── callback.py             <- functions for multi-level portfolio inline keyboard processing
    |   |   ├── inline.py               <- functions for inline buttons creation
    |   |   └── reply.py                <- functions for reply buttons creation
    |   └── log                     <- log package
    |   |   ├── __init__.py             <- configures logger client
    |   |   └── loggers.py              <- logging decorators
    |   └── validation              <- validation package
    |   |   ├── __init__.py             <- creates validation functions
    |   |   ├── formatters.py           <- formatters for better ux/ui
    |   |   ├── utils.py                <- hashing utilities for message broker
    |   |   └── validators.py           <- pydantic validator classes
    |   ├── __init__.py             <- creates cache & broker clients
    |   ├── cache.py                <- Redis based cache class
    |   ├── broker.py               <- Redis based message broker class
    |   └── creds.py                <- validates and sets environment variables
    ├── requirements.txt        <- required python packages
    ├── example.env             <- example of environment variables
    ├── README.md               <- Bot README
    ├── Dockerfile              <- creates custom bot image based on python3.9
    ├── docker-compose.yaml     <- defines multi-container Docker application
    └── app.py                  <- entrypoint

## DIY:

1. Install and activate Docker on your OS:
https://www.docker.com/get-started/

2. Download stable version of the project from **Releases**

3. Run chosen service setup in **Setups** folder:

        docker compose up -d

4. Create virtual environment and activate it in **Bot** folder:

        python3 -m venv venv
        source venv/bin/activate

5. (venv) Install dependencies:

        pip install -r requirements.txt

6. (venv) Create env file with your variables (*see example.env*) and export them:

        python3 -m venv venv
        source env

7. (venv) Run your bot:

        python3 app.py


## Fixes:

1. env file line endings should be converted when sourcing on Unix-based system venv:

        brew install dos2unix
        dos2unix /path/to/your/env_file
    
