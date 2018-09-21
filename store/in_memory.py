#!/usr/bin/env python

#===============================
#       MNEMOSINE PY CACHE
#===============================


class InMemory():
    def __init__(self):
        self.cache = {}

    def get(self, key):
        return self.cache.get(key)

    
    def put(self, key, value):
        self.cache[key] = value


    def __str__(self):
        return str(self.cache)


    
