from diskcache import Cache

# Initialize cache with expiration (1 hour)
cache = Cache("data/knowledge_cache", expiration=3600)