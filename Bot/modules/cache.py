from aioredis import Redis

from .creds import CACHE_HOST, CACHE_PORT


cache = Redis(host=CACHE_HOST,
              port=CACHE_PORT)
