#!/usr/bin/env python3
"""MRU Caching
class MRUCache that inherits from BaseCaching and is a MRU caching system
"""
BaseCaching = __import__('base_caching').BaseCaching


class MRUCache(BaseCaching):
    """class MRUCache that inherits from BaseCaching

    stack list created to track the cache use. As items in cache are reused,
    they are moved to the top of the stack, and are removed when the cache
    is full
    """
    # create class variable, stack(list) foor tracking cache use
    stack = []

    def __init__(self):
        """initialization"""
        super().__init__()

    def put(self, key, item):
        """put item in cache"""
        print(self.stack)
        # validate input
        if key is None or item is None:
            return
        # check if key in cache
        get_cache_val = self.get(key)
        if get_cache_val is None:
            # if key not in cache, check if cache is full and make space
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                del self.cache_data[self.stack[0]]
                print("DISCARD: {}".format(self.stack[0]))
                del self.stack[0]
            # add item to cache and stack
            self.cache_data[key] = item
            self.stack.append(key)
        else:  # if key in cache
            # update value of existing key
            self.cache_data[key] = item
            # update key position in stack byt moving to start
            self.stack.remove(key)
            self.stack.insert(0, key)

    def get(self, key):
        """get item from cache"""
        # validate input
        if key is None:
            return None
        if key in self.cache_data:
            # update key position in stack
            self.stack.remove(key)
            self.stack.insert(0, key)
        print(self.stack)
        return self.cache_data.get(key)
