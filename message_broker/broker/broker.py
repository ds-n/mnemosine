#!/usr/bin/env python

#===============================
#       MNEMOSINE PY EXCHANGE DISPATCHER
#===============================

from threading import Thread, Event
import queue
import logging
import time

logging.basicConfig(level=logging.INFO,
                    format='[%(threadName)-10s] %(message)s',
                    )

class Broker(Thread):

    def __init__(self, queue_name):
        Thread.__init__(self)
        self.setName(queue_name + self.__class__.__name__)
        self.setDaemon(True)
        self.subscribers = []
        self.queue_name = queue_name
        self.queue = queue.Queue()
        self.event = Event()

    def run(self):
        
        while True:
            errors = 0
            logging.info("LifeCycle<start> - Queue Q(%r) contains approximately %r messages. Event(%r)" % (self.queue_name, self.queue.qsize(), self.event.is_set()))
            if self.event.is_set() is False:
                logging.info("Waiting for a subscriber for the queue Q(%r)" % self.queue_name)

            self.event.wait()
            message = self.queue.get()
            logging.info("LifeCycle<reading> - Getting message (%s) from Q(%r)" % (message, self.queue_name))

            num_subscribed = len(self.subscribers)
            logging.info("LifeCycle<sending> - Sending message (%s) from Q(%r) to N°(%s) subscribers" % (message, self.queue_name, num_subscribed))
            for subscriber in self.subscribers:
                try:
                    subscriber.send(message.encode())
                except Exception as e:
                    logging.info(e)
                    #todo remove this subriber from the list
                    errors = errors + 1
                    self.subscribers.remove(subscriber)
                    
            logging.info("LifeCycle<status> - Errors(%s) / n°subscribers(%s)" % (errors, num_subscribed))
            if errors == num_subscribed:
                self.publish(message) #republish message if non send at almost 1 subscriber
                logging.info("LifeCycle<republish> - Republish Message(%r) into queue Q(%r)" % (message, self.queue_name))
                
            if(len(self.subscribers)) == 0:
                self.event.clear()
                logging.info("LifeCycle<stopping> - Stopping thread and attends for a subscriber for the queue Q(%r)" % self.queue_name)
            self.queue.task_done()
            time.sleep(0.5)
            logging.info("LifeCycle<finish> - Queue Q(%r) contains approximately %r messages. Event(%r)" % (self.queue_name, self.queue.qsize(), self.event.is_set()))

    
    def publish(self, message):
        self.queue.put(message)
        
    def subscribe(self, connection):
        self.subscribers.append(connection)
        self.event.set()
        logging.info("Subscribed event set %r" % self.event.is_set())
