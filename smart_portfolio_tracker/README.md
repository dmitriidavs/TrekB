<div align="center">

# TrekB
### *Smart Portfolio Tracker*

A bot powered by modern data engineering and infrastructure solutions,\
designed to allow easy performance tracking of your digital assets\
via simple Telegram interfaces. **Try it out yourself:**\
[ COMING VERY SOON xD ]

<a href="https://t.me/TrekB_bot">
  <img src="Misc/pics/TrekB_logo.png" alt="TrekB Logo" title="https://t.me/TrekB_bot" style="width:10% ; height:10%">
</a>

</div>

## Repository Organization:

    ├── README.md               <- Project README
    ├── Bot                     <- Core Telegram "front-end" component of the project 👨‍💻
    ├── Bot_placeholder         <- Interim "front-end" runner while Bot is in DEV ✔️
    ├── VM                      <- VM based solution
    ├── Cloud                   <- Cloud based solution
    ├── Lite                    <- Quick-start solution with some basic features 👨‍💻
    ├── Misc                    <- Miscellaneous secondary objects
    └── Research                <- Some research on maths, statistics & metrics logic

<div align="center">

[About](#about) •
[Capabilities](#capabilities) •
[Architecture](#architecture) •
[Scaling](#scaling) •
[Takeaways](#takeaways) •
[Links](#links)

</div>

## About

To be updated ...

## Capabilities
    
<ins>Implemented</ins>

    • [LITE]: add, edit & delete individual asset records in portfolio
    
<ins>Upcoming</ins>

    • [VM]: improved portfolio navigation
    • [VM]: import crypto wallet balance & history into portfolio

## Architecture

### [LITE]

MVP version of the project which enables users to manage their asset portfolios.

<ins>Tech Features</ins>

    • asynchronous I/O
    • DB keeps users' info & handles portfolio management
    • Redis caching is used to optimize DB* querying
    • users' input data is validated with pydantic
    • DB* querying performance & users' actions are logged to either CLI, local folder or logging service
    
      * DB - transactional DB (SQLite in [LITE] & PostgreSQL in [VM])
    
<ins>High-Level Overview</ins>

<ins>Telegram Component</ins>

<ins>Database Component</ins>

<ins>Screenshots</ins>

Stack: `SQLite`, `Redis`, `Python`, `SQL`, `Docker`

---

### [VM]

Main version of the projects which enables users to gain insights on their portfolios.

<ins>Tech Features</ins>

    Everything from [LITE] plus:
    • 

<ins>High-Level Overview</ins>

![VM Architecture](Misc/pics/arch_high_lvl.png?raw=true "VM Architecture")

Stack: `PostgreSQL`, `SQLite [Lite]`, `Redis`, `Apache Airflow`, `MinIO S3`, `Docker`,
`Python`, `SQL`

<ins>Telegram Component</ins>

![Telegram Component](Misc/pics/arch_tg.png?raw=true "Telegram Component")

Tags: `tag1`

<ins>Database Component</ins>

<ins>Data Pipelines</ins>

<ins>Docker Layers & Networking</ins>

<ins>CI/CD Component</ins>

---

### [CLOUD]

A migration of VM based solution to AWS cloud architecture.

Stack: `- AWS? Azure? - Excel!`, `Python`, `SQL`

## Scaling

To be updateted ...

## Takeaways

To be updateted ...

## Links

Libraries:
[`aiogram`](https://github.com/aiogram/aiogram),
[`asyncio`](https://github.com/python/asyncio),
[`aiosqlite`](https://github.com/omnilib/aiosqlite),
[`SQLAlchemy`](https://github.com/sqlalchemy/sqlalchemy),
[`pydantic`](https://github.com/pydantic/pydantic),
[`redis`](https://github.com/redis/redis),
[`aioredis`](https://github.com/aio-libs/aioredis-py)

Projects:
[`SQLite`](https://sqlite.org/index.html),
[`Redis`](https://redis.io/)



<div align="center">

Designed & Developed by: [@dmitriidavs](https://t.me/dmitriidavs)

</div>
