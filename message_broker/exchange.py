#!/usr/bin/env python

#===============================
#       MNEMOSINE PY EXCHANGE
#===============================

from threading import Thread
import queue
import logging
import uuid
from message_broker.broker.broker import Broker

logging.basicConfig(level=logging.INFO,
                    format='[%(threadName)-10s] %(message)s',
                    )



class Exchange(object):

    def __init__(self):
        self.brokers = {}

            
    def publish(self, queue_name, message, connection):
        if self.brokers.get(queue_name) is None:
            broker = Broker(queue_name)
            broker.start()
            self.brokers[queue_name] = broker

        self.brokers[queue_name].publish(message)
        connection.close()

    def subscribe(self, queue_name, connection):
        if self.brokers.get(queue_name) is None:
            broker = Broker(queue_name)
            broker.start()
            self.brokers[queue_name] = broker

        self.brokers[queue_name].subscribe(connection)
