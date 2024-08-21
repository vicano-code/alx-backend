#!/usr/bin/env python3
"""LIFO Caching
a class LIFOCache that inherits from BaseCaching and is a LIFO caching system
"""
BaseCaching = __import__('base_caching').BaseCaching


class LIFOCache(BaseCaching):
    """class LIFOCache that inherits from BaseCaching
    """
    def __init__(self):
        """initialization"""
        super().__init__()

    def put(self, key, item):
        """put data in cache"""
        if key or item is not None:
            get_cache_val = self.get(key)
        if get_cache_val is None:
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                key_list = list(self.cache_data.keys())
                del_idx = len(key_list) - 1
                print("DISCARD: {}".format(key_list[del_idx]))
                del self.cache_data[key_list[del_idx]]
        else:
            # delete item if key exists in cache
            del self.cache_data[key]
        # add item to cache
        self.cache_data[key] = item

    def get(self, key):
        """get cache data"""
        if key is None:
            return None

        return self.cache_data.get(key)
