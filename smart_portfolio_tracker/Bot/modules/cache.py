from aioredis import Redis

from .creds import UTIL_DB_HOST, UTIL_DB_PORT


cache = Redis(host=UTIL_DB_HOST,
              port=UTIL_DB_PORT)
