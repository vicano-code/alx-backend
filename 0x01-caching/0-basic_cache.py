#!/usr/bin/env python3
"""Basic dictionary
class BasicCache that inherits from BaseCaching and is a caching system
"""
BaseCaching = __import__('base_caching').BaseCaching


class BasicCache(BaseCaching):
    """A basic Cache class
    """
    def put(self, key, item):
        """put data in cache"""
        if key or item is not None:
            self.cache_data[key] = item

    def get(self, key):
        """get cache data"""
        if key is None:
            return None
        if key not in self.cache_data.keys():
            return None
        return self.cache_data.get(key)
