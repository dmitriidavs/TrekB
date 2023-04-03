from aioredis import Redis

from .creds import BROKER_HOST, BROKER_PORT


broker = Redis(host=BROKER_HOST,
               port=BROKER_PORT,
               decode_responses=True)
