#!/usr/bin/env python

#===============================
#       MNEMOSINE PY DEFINITION
#===============================

from enum import Enum

class Body():
    def __init__(self, key, value, connection):
        self.key = key
        self.value = value
        self.connection = connection

class MetaEnum(Enum):
    STORE = "store"
    GET = "get"
    PUT = "put"
    PUBLISH = "publish"
    SUBSCRIBE = "subscribe"
    NONE = ""
    

class Meta():
    def __init__(self, task, method):
        self.task = MetaEnum(task)
        self.method = MetaEnum(method)

class Data ():
    def __init__(self, meta, body):
        self.meta = meta
        self.body = body
