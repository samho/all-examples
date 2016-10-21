#!/usr/bin/env python
import pika
import datetime
import time
import sys


def publish_message(_host="localhost", _routing_key='task_queue', _message="Hello World!"):
    connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=_host))
    channel = connection.channel()

    channel.queue_declare(queue='task_queue', durable=False)

    message = ' '.join(_message) or "Hello World!"
    channel.basic_publish(exchange='',
                          routing_key=_routing_key,
                          body=message,
                          properties=pika.BasicProperties(
                             delivery_mode=2,  # make message persistent
                          ))
    print " [x] Sent %r" % (message,)
    connection.close()


def main():
    while True:
        print "Press Ctrl+C to stop publishing."
        msg = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        publish_message(msg)
        time.sleep(5)


if __name__ == "__main__":
    main()


