from aioredis import Redis

from .creds import BROKER_HOST, BROKER_PORT


cache = Redis(host=BROKER_HOST,
              port=BROKER_PORT)
