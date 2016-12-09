import cPickle
import datetime
import json
import os
import random
import sys
import time

from profanity import profanity
import requests
import tweepy

import helper_functions

# connect to redis
r = helper_functions.connect_redis_db()

# connect to twitter api
CONSUMER_KEY=os.getenv('CONSUMER_KEY',None)
CONSUMER_SECRET=os.getenv('CONSUMER_SECRET',None)
ACCESS_TOKEN=os.getenv('ACCESS_TOKEN',None)
ACCESS_TOKEN_SECRET=os.getenv('ACCESS_TOKEN_SECRET',None)
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)
terms = ['python','steph curry','cloud foundry','pivotal','new york','data science', 'javascript',
         'machine learning', 'wonderful', 'algorithm', 'java', 'programming']

# load synthetic tweets for backup
syn_tweets = cPickle.load(open('status-11-17-2016.pkl'))

class CustomStreamListener(tweepy.StreamListener):

    """Source: http://www.brettdangerfield.com/post/realtime_data_tag_cloud/ """
    def __init__(self, api):
        self.api = api
        self.tweet_list = []
        self.score_tweet_time = time.time()
        self.write_to_redis_time = time.time()
        self.p = 0.5
        self.score_post_int = 0.5
        self.write_to_redis_int = 5
        super(tweepy.StreamListener, self).__init__()

    def compute_polarities(self, tweet_list):
        url = 'http://sentiment-compute-app.cfapps.pez.pivotal.io/polarity_compute'
        # url = 'http://127.0.0.1:8001/polarity_compute'
        ps = requests.post(url, json={"data": self.tweet_list}).json()['polarity']
        return ps

    def save_posted_tweet_to_redis(self, tweet, p, source):
        msg = json.dumps({'text': profanity.censor(tweet),  # for public dashboard
                          'polarity': p,
                          'source': source})
        r.publish('tweet_msgs', msg)

    def english_tweet(self, tweet):
        return tweet.lang == 'en'

    def emulate_tweet(self):
        '''Send a fake tweet using previously saved tweets'''
        # hack
        self.on_status(random.choice(syn_tweets), source = 'emulated')

    def on_status(self, status, source = 'live'):
        global full_tweet
        global cur_tweet
        global cur_p

        full_tweet = status
        del_time = full_tweet.created_at - datetime.datetime.utcnow()
        # print del_time.total_seconds()
        if not self.english_tweet(status):
            return
        # print status.text
        self.tweet_list.append(status.text)
        time_since_last_score = (time.time() - self.score_tweet_time)
        if time_since_last_score > self.score_post_int:
            # score sentiment
            ps = self.compute_polarities(self.tweet_list)
            # for sentiment plot on dashboard - using average polarity per second (js code queries every second)
            mean_ps = sum(ps)/(1.0*len(ps))
            r.lpush('polarity', json.dumps({'time': time.time(), 'polarity': mean_ps}))
            cur_tweet = self.tweet_list[-1]
            cur_p = ps[-1]
            self.score_tweet_time = time.time()
            self.tweet_list = []
        # for posting to dashboard every n seconds
        time_since_last_redis_write = (time.time() - self.write_to_redis_time)
        if time_since_last_redis_write > self.write_to_redis_int:
            self.save_posted_tweet_to_redis(cur_tweet,cur_p,source)
            self.write_to_redis_time = time.time()


    def on_error(self, status_code):
        print >> sys.stderr, 'Encountered error with status code:', status_code
        return True  # Don't kill the stream

    def on_timeout(self):
        print >> sys.stderr, 'Timeout...'
        return True  # Don't kill the stream

stream = tweepy.streaming.Stream(auth, CustomStreamListener(api))
emulate_time = 60
while True:
    try:
        print 'Connecting to Twitter Firehose'
        stream.filter(track = terms, stall_warnings=True, filter_level="low")
    except (KeyboardInterrupt, Exception), e:
        print e
        print 'Emulating tweets for {} seconds'.format(emulate_time)
        stream.disconnect()
        start_time = time.time()
        while (time.time() - start_time) < emulate_time:
            time.sleep(random.random())
            stream.listener.emulate_tweet()
