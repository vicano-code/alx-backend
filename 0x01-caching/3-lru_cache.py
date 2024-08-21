#!/usr/bin/env python3
"""LRU Caching
class LRUCache that inherits from BaseCaching and is a LRU caching system
"""
BaseCaching = __import__('base_caching').BaseCaching


class LRUCache(BaseCaching):
    """class LRUCache that inherits from BaseCaching

    queue list created to track the cache use. As items in cache are reused,
    they are moved to the end of the queue, while the least recently used
    items remain at the front of queue according to when they are added.
    """
    # create class variable, queue (list) foor tracking cache use
    queue = []

    def __init__(self):
        """initialization"""
        super().__init__()

    def put(self, key, item):
        """put item in cache"""
        # validate input
        if key is None or item is None:
            return
        # check if key in cache
        get_cache_val = self.get(key)
        if get_cache_val is None:
            # if key not in cache, check if cache is full and make space
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                del self.cache_data[self.queue[0]]
                print("DISCARD: {}".format(self.queue[0]))
                del self.queue[0]
            # add item to cache and queue
            self.cache_data[key] = item
            self.queue.append((key))
        else: # if key in cache
            # update value of existing key
            self.cache_data[key] = item
            # update key position in queue by moving to end
            self.queue.remove(key)
            self.queue.append(key)               

    def get(self, key):
        """get item from cache"""
        # validate input
        if key is None:
            return None
        if key in self.cache_data:
            # update key position in queue by moving to end
            self.queue.remove(key)
            self.queue.append(key)

        return self.cache_data.get(key)
