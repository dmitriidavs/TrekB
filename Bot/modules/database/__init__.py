__all__ = ['queries_portfolio', 'queries_user', 'logic_portfolio', 'logic_user',
           'DBMSCreateConnection']

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
