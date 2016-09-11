#!/usr/bin/env python
import pika
import datetime
import time


def publish_message(_message="Hello World!"):
    connection = pika.BlockingConnection(pika.ConnectionParameters(
            host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='task_queue', durable=True)

    message = ' '.join(_message) or "Hello World!"
    channel.basic_publish(exchange='',
                          routing_key='task_queue',
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


