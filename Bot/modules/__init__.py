__all__ = ['broker', 'cache', 'creds']

from .creds import (
    CACHE_HOST, CACHE_PORT, CACHE_TTL,
    BROKER_HOST, BROKER_PORT, BROKER_TTL
)
from .broker import Broker
from .cache import Cache


broker = Broker(host=BROKER_HOST,
                port=BROKER_PORT,
                decode_responses=True,
                broker_ttl=BROKER_TTL)

cache = Cache(host=CACHE_HOST,
              port=CACHE_PORT,
              cache_ttl=CACHE_TTL)
