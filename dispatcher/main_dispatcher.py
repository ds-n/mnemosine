#!/usr/bin/env python

#===============================
#       MNEMOSINE PY DISPATCHER
#===============================

from threading import Thread
import queue
import logging
import time
from store.store_worker import StoreWorker
from meta.meta import MetaEnum
from message_broker.exchange import Exchange
logging.basicConfig(level=logging.INFO,
                    format='[%(threadName)-10s] %(message)s',
                    )

class MainDispatcher(Thread):

    def __init__(self):
        Thread.__init__(self)
        self.setName(self.__class__.__name__)
        self.setDaemon(True)
        self.queue = queue.Queue()
        self.store_worker = StoreWorker()
        self.store_worker.start()

        self.exchange = Exchange()

    def run(self):
        
        while True:
            item = self.queue.get()
            logging.info("Getting item %r" % item)
            logging.info("switch task item %r" % item.meta.task)

            if item.meta.task is MetaEnum.STORE:
                self.store_worker.put(item)
            if item.meta.task is MetaEnum.PUBLISH:
                self.exchange.publish(item.body.key, item.body.value, item.body.connection)
            if item.meta.task is MetaEnum.SUBSCRIBE:
                self.exchange.subscribe(item.body.key, item.body.connection)
            
            self.queue.task_done()
            time.sleep(0.5)

    def dispatch(self, item):
        logging.info("Putting item in queue to dispatch %r" % item)
        self.queue.put(item)
