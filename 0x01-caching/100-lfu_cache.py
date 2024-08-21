#!/usr/bin/env python3
"""LFU Caching
class LFUCache that inherits from BaseCaching and is a LFU caching system
"""
from collections import OrderedDict
BaseCaching = __import__('base_caching').BaseCaching


class LFUCache(BaseCaching):
    """class LFUCache that inherits from BaseCaching

    frequency dict object created to track item use frequency in cache.
    """
    # create class variable, freq (dict) for tracking cache use
    freq = OrderedDict()

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
                # get least frequently used key
                first_key, first_value = next(iter(self.freq.items()))
                count = first_value
                del_key = first_key
                for k, v in self.freq.items():
                    if v < count:
                        count = v
                        del_key = k
                del self.cache_data[del_key]
                print("DISCARD: {}".format(del_key))
                del self.freq[del_key]
            # add item to cache and freq
            self.cache_data[key] = item
            self.freq[key] = 1
        else: # if key in cache
            # update value of existing key
            self.cache_data[key] = item
            # update key freq
            self.freq[key] += 1          

    def get(self, key):
        """get item from cache"""
        # validate input
        if key is None:
            return None
        if key in self.cache_data:
           # update key freq
            self.freq[key] += 1

        return self.cache_data.get(key)
