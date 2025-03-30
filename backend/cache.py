from cachetools import TTLCache

# Cache: Stores last 100 queries for 10 minutes
cache = TTLCache(maxsize=100, ttl=600)

def get_cached_result(query):
    """Fetches result from cache if available."""
    return cache.get(query)

def set_cached_result(query, result):
    """Caches search result."""
    cache[query] = result
