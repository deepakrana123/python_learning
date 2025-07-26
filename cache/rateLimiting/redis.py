import redis
import time
from .luascript import SLIDING_WINDOW_LUA

redis_client = redis.Redis()

script_sha = redis_client.script_load(SLIDING_WINDOW_LUA)
