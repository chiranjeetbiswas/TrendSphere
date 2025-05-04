from flask_caching import Cache

cache = Cache(config={
    'CACHE_TYPE': 'simple',
    'CACHE_DEFAULT_TIMEOUT': 300
})

# Cache keys for each platform
CACHE_KEYS = {
    'twitter': 'twitter_trends',
    'youtube': 'youtube_trends_{region}',
    'reddit': 'reddit_trends_{subreddit}',
    'hackernews': 'hackernews_trends',
    'googlenews': 'googlenews_trends',
    'producthunt': 'producthunt_trends'
}

def get_cached_trends(platform, fetch_function, *args, **kwargs):
    """Get trends from cache or fetch and cache if not available"""
    cache_key = CACHE_KEYS.get(platform)
    if not cache_key:
        return fetch_function(*args, **kwargs)
    
    # Format cache key with region for YouTube
    if platform == 'youtube' and 'region' in kwargs:
        cache_key = cache_key.format(region=kwargs['region'])
    elif platform == 'youtube' and len(args) > 0:
        cache_key = cache_key.format(region=args[0])
    # Format cache key with subreddit for Reddit
    elif platform == 'reddit' and 'subreddit' in kwargs:
        cache_key = cache_key.format(subreddit=kwargs['subreddit'] or 'all')
    elif platform == 'reddit' and len(args) > 0:
        cache_key = cache_key.format(subreddit=args[0] or 'all')
    # Format cache key with category for Product Hunt
    elif platform == 'producthunt' and 'category' in kwargs:
        cache_key = cache_key.format(category=kwargs['category'] or 'all')
    elif platform == 'producthunt' and len(args) > 0:
        cache_key = cache_key.format(category=args[0] or 'all')
    
    # Try to get from cache
    cached_data = cache.get(cache_key)
    if cached_data:
        return cached_data
    
    # If not in cache, fetch and store
    data = fetch_function(*args, **kwargs)
    cache.set(cache_key, data)
    return data

def clear_platform_cache(platform, region=None, subreddit=None, category=None):
    """Clear cache for a specific platform"""
    cache_key = CACHE_KEYS.get(platform)
    if not cache_key:
        return
    
    if platform == 'youtube' and region:
        cache_key = cache_key.format(region=region)
        cache.delete(cache_key)
    elif platform == 'reddit' and subreddit:
        cache_key = cache_key.format(subreddit=subreddit or 'all')
        cache.delete(cache_key)
    elif platform == 'producthunt' and category:
        cache_key = cache_key.format(category=category or 'all')
        cache.delete(cache_key)
    else:
        cache.delete(cache_key)

def clear_all_cache():
    """Clear all platform caches"""
    for cache_key in CACHE_KEYS.values():
        if '{region}' in cache_key:
            # For YouTube, we need to clear all region-specific caches
            for region in ['US', 'GB', 'IN', 'JP', 'KR', 'BR', 'DE', 'FR']:
                cache.delete(cache_key.format(region=region))
        else:
            cache.delete(cache_key) 