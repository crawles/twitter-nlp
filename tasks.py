import json
import time

import pandas as pd
import requests

import helper_functions

r = helper_functions.connect_redis_db()

def gen_tweet_stats():
    time_interval = 1
    while True:
        time_start = time.time()
        url = 'http://sentiment-compute-metrics.cfapps.pez.pivotal.io/tweet_rate'
        tr = requests.get(url, {'time_interval': time_interval}).content

        url = 'http://sentiment-compute-metrics.cfapps.pez.pivotal.io/avg_sentiment'
        avg_polarity = requests.get(url, {'time_interval': time_interval}).content
        while not helper_functions.been_n_second(.98, time.time(), time_start, wait_time=.01):
            pass

        r.publish('tweet_stats', json.dumps({'tweet_rate': tr, 'avg_polarity': avg_polarity}))
        print tr