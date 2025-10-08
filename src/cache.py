import redis
import json
from datetime import timdelta 


cache = redis.Redis(host ="localhost", port = 6379, db =0)

def get_cached_response(key):
    data = cache.get(key)
    return json.loads(data) if data else None

def set_cached_response(key, data, ttl=3600):
    cache.setex(key, timdelta(Second=ttl), json.dumps(data))