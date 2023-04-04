__all__ = ['broker', 'cache', 'creds']

from .creds import (
    CACHE_HOST, CACHE_PORT,
    BROKER_HOST, BROKER_PORT
)
from .broker import Broker
from .cache import Cache


broker = Broker(host=BROKER_HOST,
                port=BROKER_PORT,
                decode_responses=True)

cache = Cache(host=CACHE_HOST,
              port=CACHE_PORT)
