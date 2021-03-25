# -*- coding: utf-8 -*-
"""
Created on Tue Mar  2 13:00:32 2021

@author: Creighton
"""

import pika
import sys
import os

# The base class message queue
# Contains functionality for sending and receiving messages
# Requires Pika library to be installed and RabbitMQ server running


class MessageQueue:

    def __init__(self):
        self.ip = 'localhost'

        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(self.ip))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='default')

    def send(self, message):
        self.channel.basic_publish(
            exchange='', routing_key='default', body=message)

    def receive(self, callback):

        self.channel.basic_consume(
            queue='default', auto_ack=True, on_message_callback=callback)

        self.channel.start_consuming()

    def close(self):
        self.connection.close()
