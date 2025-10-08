import redis
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

# We'll use a dummy cache if Redis is not available
class DummyCacheBackend:
    async def get(self, key):
        return None
    
    async def set(self, key, value, expire=None):
        pass
    
    async def clear(self, namespace=None):
        pass

def setup_cache(app: FastAPI):
    """
    Initialize the cache on application startup
    """
    @app.on_event("startup")
    async def startup_event():
        try:
            r = redis.Redis(host='localhost', port=6379, db=0)
            r.ping()
            FastAPICache.init(RedisBackend(r), prefix='fastapi-cache')
            print("Redis cache initialized successfully")
        except redis.exceptions.ConnectionError:
            # Use dummy cache if Redis is not available
            print("Warning: Redis server not available. Using in-memory dummy cache.")
            FastAPICache.init(DummyCacheBackend(), prefix='fastapi-cache')
        except Exception as e:
            print(f"Error initializing cache: {e}")
            # Still use dummy cache in case of other errors
            FastAPICache.init(DummyCacheBackend(), prefix='fastapi-cache')