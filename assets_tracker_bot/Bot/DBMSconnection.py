from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession


class DBMSCreateConnection:
    """Async DMBS session connection class"""

    def __init__(self, connection_string):
        self.connection_str = connection_string
        self.session = None

    def __enter__(self):
        engine = create_engine(self.connection_str)
        session = sessionmaker()
        self.session = session(bind=engine)

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()

    # async def __aenter__(self):
    #     engine = create_async_engine(self.connection_str)
    #     self.session = AsyncSession(bind=engine)
    #
    #     return self
    #
    # async def __aexit__(self, exc_type, exc_val, exc_tb):
    #     self.session.close()
