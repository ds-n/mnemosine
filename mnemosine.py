#!/usr/bin/env python

#===============================
#       MNEMOSINE PY
#===============================


import socket
import logging
import json
from enum import Enum
from dispatcher.main_dispatcher import MainDispatcher
from meta.meta import Meta, Body, Data

logging.basicConfig(level=logging.INFO,
                    format='[%(threadName)-10s] %(message)s',
                    )





    


class Server():
    def __init__(self, tcp_ip='127.0.0.1', tcp_port=5005):
        self.tcp_ip = tcp_ip
        self.tcp_port = tcp_port
        self.buffer_size = 1024  # Normally 1024, but we want fast response
        self.dispatcher = MainDispatcher()
        self.dispatcher.start()

    def listen(self):
        logging.info('TCP_IP address:%s' % self.tcp_ip)
        sck = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sck.bind((self.tcp_ip, self.tcp_port))
        sck.listen(1)
        while True:
            connection, address = sck.accept()
            string = connection.recv(self.buffer_size)
            dictionary = json.loads(string)
            meta = Meta(dictionary['meta']['task'], dictionary['meta']['method'])
            body = Body(dictionary['body']['key'], dictionary['body']['value'], connection)
            
            logging.info("Meta Task(%s)" % meta.task)
            logging.info("Meta Method(%s)" % meta.method)
            logging.info("Body Key(%s)" % body.key)
            logging.info("Body Value(%s)" % body.value)
            data = Data(meta, body)
            self.dispatcher.dispatch(item=data)



server = Server()
server.listen()
    
