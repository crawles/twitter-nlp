#!/usr/bin/env python
import json
import pika

host = 'localhost'
exchange = ''
queue = 'twitter2sentiment'

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=host))
channel = connection.channel()

#channel.queue_declare(queue=queue)
tweets = []
def callback(ch, method, properties, body):
    jmsg = json.loads(body)
    if 'text' in jmsg.keys():
        print(jmsg)
    tweets.append(jmsg)
    #print(" [x] Received %r" % body)

channel.basic_consume(callback,
                      queue=queue,
                      no_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()