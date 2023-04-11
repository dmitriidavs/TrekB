<div align="center">

# TrekB
### *Smart Portfolio Tracker*

A bot powered by modern data engineering and infrastructure solutions,\
designed to allow easy performance tracking of your digital assets\
via simple Telegram interfaces. **Try it out yourself:**

<a href="https://t.me/TrekB_bot">
  <img src="Misc/pics/TrekB_logo.png" alt="TrekB Logo" title="https://t.me/TrekB_bot" style="width:10% ; height:10%">
</a>

</div>

## Repository Organization:
    
    ├── .github                 <- CI/CD workflows
    ├── AWS                     <- AWS services code
    ├── Airflow                 <- Airflow dags code
    ├── Bot                     <- Telegram Bot code
    └── Misc                    <- Miscellaneous items

<div align="center">

[Capabilities](#capabilities) •
[Architecture](#architecture) •
[Scaling](#scaling) •
[Takeaways](#takeaways) •
[Links](#links)

</div>

## Capabilities
    
<ins>Implemented</ins>

    • [LITE]: add, edit & delete individual asset records in portfolio
    
<ins>Upcoming</ins>

    • [MAIN]: improved portfolio navigation
    • [MAIN]: import crypto wallet balance & history into portfolio

## Architecture

### [LITE]

MVP version of the project which enables users to manage their asset portfolios.

<ins>Tech Features</ins>

    • asynchronous I/O
    • DB* keeps users' info & handles portfolio management
    • Redis cache is used for DB* querying optimization & keeping dialogue FSM states
    • Redis message broker is used for data transmission between callbacks
    • DB* querying performance & users' actions are logged to either CLI, local folder or logging service
    • users' input data is validated with pydantic
    • deployed with Docker Compose on EC2
    
      * DB - OLTP DB (SQLite in [LITE] & RDS PostgreSQL in [MAIN])
    
<ins>System Design</ins>

![LITE Architecture](Misc/pics/lite_arch.png?raw=true "LITE Architecture")

Tags: `SQLite`, `Redis`, `Python`, `SQL`, `Docker Compose`, `EC2`

<ins>DB Dependencies</ins>

![LITE Dependencies](Misc/pics/lite_db_diagram.png?raw=true "LITE Dependencies")

---

### [MAIN]

Primary version of the projects which enables users to gain insights on their portfolios.

<ins>Tech Features</ins>

    Everything from [LITE] plus:
    • 

<ins>System Design</ins>

![VM Architecture](Misc/pics/arch_high_lvl.png?raw=true "High-Level Architecture")

Tags: `ClickHouse`, `RDS PostgreSQL`, `Redis`, `Apache Kafka & Debezium`, `Apache Airflow`, `S3`, `Python`, `SQL`, `Docker Compose`, `EC2`

<ins>Data Pipelines</ins>

![Data Pipelines](Misc/pics/data_pipelines.png?raw=true "Data Pipelines")

Tags: `OLAP`, `OLTP`, `Orchestration`, `Message Broker`, `Cache`, `Webhook`, `Logging`, `Data Buckets`, `Data Discovery`, `CDC`, `Web3`, `API`

<ins>DB Dependencies</ins>

<ins>Orchestration</ins>

<ins>Networking</ins>

---

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
[`Redis`](https://redis.io/),
[`Docker`](https://www.docker.com/)



<div align="center">

Designed & Developed by: [@dmitriidavs](https://www.linkedin.com/in/dmitriidavs/)

</div>
