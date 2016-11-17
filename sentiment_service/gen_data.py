"""
For testing - a synthetic Twitter source
"""
import time

import json
import pandas as pd
import pika
import sys
import tweepy

host = 'localhost'
exchange = ''
queue = 'twitter2sentiment'

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost')
)
channel = connection.channel()
args = {"x-max-length": 2000}
channel.queue_declare(queue=queue, arguments=args)

tweets_list = pd.read_pickle('tweets_list.pkl')
while True:
   for t in tweets_list:
       channel.basic_publish(exchange=exchange,
                             routing_key=queue,
                             body=str(json.dumps(t)))
       print(t['text'])
       time.sleep(2.5)

# real data

# class CustomStreamListener(tweepy.StreamListener):
#     """Source: http://www.brettdangerfield.com/post/realtime_data_tag_cloud/ """
#     def __init__(self, api):
#         self.api = api
#         super(tweepy.StreamListener, self).__init__()
#
#         #setup rabbitMQ Connection
#         connection = pika.BlockingConnection(
#             pika.ConnectionParameters(host = host)
#         )
#         self.channel = connection.channel()
#
#         #set max queue size
#         args = {"x-max-length": 2000}
#
#         self.channel.queue_declare(queue=queue, arguments=args)
#
#     def on_status(self, status):
#         print status.text, "\n"
#
#         data = {}
#         data['text'] = status.text
#         data['created_at'] = time.mktime(status.created_at.timetuple())
#         data['geo'] = status.geo
#         data['source'] = status.source
#
#         #queue the tweet
#         self.channel.basic_publish(exchange=exchange,
#                                     routing_key=queue,
#                                     body=json.dumps(status._json))
#
#     def on_error(self, status_code):
#         print >> sys.stderr, 'Encountered error with status code:', status_code
#         return True  # Don't kill the stream
#
#     def on_timeout(self):
#         print >> sys.stderr, 'Timeout...'
#         return True  # Don't kill the stream
#
# # connect to twitter
# # parameters
# consumer_key = 'Yan2bmh6PQLUgCOcWgUYs5Ahh'
# consumer_secret = 'oJH7hzLYxu5KRf0Rx9FiD7y6UIqetnPNwtaxlPX6DRptZllBKX'
# access_token = '47235146-mgdnyeAG2tubNL1QFvLe4HQxO9igODD3yMCwdKUX1'
# access_token_secret = 'pJUjByCSGSBj3704plWZw84ftmt1e1n3M44rhczybon8O'
#
# auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
# auth.set_access_token(access_token, access_token_secret)
# api = tweepy.API(auth)
#
# sapi = tweepy.streaming.Stream(auth, CustomStreamListener(api))
# sapi.filter(track=['chelsea'])