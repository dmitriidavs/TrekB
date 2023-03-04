"""
TrekB | Smart Portfolio Tracker
:copyright: (c) 2023 by Dmitrii Davletshin (@dmitriidavs)
:license: BSD-3-Clause, see LICENSE for more details
"""

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession


class DBMSCreateConnection:
    """Async DBMS session context manager"""

    def __init__(self, connection_string):
        self.connection_str = connection_string
        self.session = None

    async def __aenter__(self):
        engine = create_async_engine(self.connection_str)
        self.session = AsyncSession(bind=engine)

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()
