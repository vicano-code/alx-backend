#!/usr/bin/nv python3
"""FIFO caching
a class FIFOCache that inherits from BaseCaching and is a FIFO caching system
"""
BaseCaching = __import__('base_caching').BaseCaching


class FIFOCache(BaseCaching):
    """FiFO cache system class that iherits from BaseCaching
    """
    def __init__(self):
        """initialization"""
        super().__init__()

    def put(self, key, item):
        """put data in cache"""
        if key or item is not None:
            self.cache_data[key] = item
        if len(self.cache_data) > BaseCaching.MAX_ITEMS:
            firstKey = next(iter(self.cache_data))
            print("DISCARD: {}".format(firstKey))
            del self.cache_data[firstKey]

    def get(self, key):
        """get cache data"""
        if key is None:
            return None

        return self.cache_data.get(key)
