#!/usr/bin/env python

#===============================
#       MNEMOSINE PY STORE WORKER
#===============================

from threading import Thread
import queue
import logging
import time
from store.in_memory import InMemory
from meta.meta import MetaEnum
import json
import base64

logging.basicConfig(level=logging.INFO,
                    format='[%(threadName)-10s] %(message)s',
                    )

class StoreWorker(Thread):

    def __init__(self):
        Thread.__init__(self)
        self.setName(self.__class__.__name__)
        self.setDaemon(True)
        self.queue = queue.Queue()
        self.cache = InMemory()

    def run(self):
        
        while True:
            item = self.queue.get()
            
            logging.info("switch task item %r" % item.meta.task)

            if item.meta.method is MetaEnum.GET:
                
                value = self.cache.get(item.body.key)
                logging.info("Getting item %r:%r" % (item.body.key, value))
                if value is None:
                    value = ''
                item.body.connection.send(self.decode(value))
                
            if item.meta.method is MetaEnum.PUT:
                value = self.encode(item.body.value)
                self.cache.put(item.body.key, value)
                logging.info("Putting item %r:%r" % (item.body.key, value))

            item.body.connection.close()
            logging.info(self.cache)    
            self.queue.task_done()
            time.sleep(0.5)

    def encode(self, value):
        
        return base64.b64encode(json.dumps(value).encode())

    def decode(self, value):
        return base64.b64decode(value)
        
    def put(self, item):
        logging.info("Putting item in queue to attends to accesse the store %r" % item)
        self.queue.put(item)
