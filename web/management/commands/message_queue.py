# -*- coding: utf-8 -*-
"""
Created on Tue Mar  2 13:00:32 2021

@author: Creighton
"""

import pika, sys, os

# The base class message queue
# Contains functionality for sending and receiving messages
# Requires Pika library to be installed and RabbitMQ server running

class MessageQueue:
    
    def __init__(self, message):
        self.ip = 'localhost'
        self.message = message
        
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(self.ip))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='default')
    
    def send(self, message):
        
        #message = ' '.join(sys.argv[1:]) or "Default Message"
        
        self.channel.basic_publish(exchange='',routing_key='default',body=message)
        print(" [x] Sent '" + message + "'")
        
        self.connection.close()

    def receive(self, message):
        try:        
            def callback(ch, method, properties, body):
                print(" [x] Received %r" % body.decode())
            
            self.channel.basic_consume(queue='default',auto_ack=True,on_message_callback=callback)
            
            print(' [*] Waiting for messages. To exit press CTRL+C')
            self.channel.start_consuming()
        except KeyboardInterrupt:
            print('Interrupted')
            try:
                sys.exit(0)
            except SystemExit:
                os._exit(0)
