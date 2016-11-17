import json
import os
import time

from flask import Flask, request, jsonify
import pandas as pd
import redis

import helper_functions

app = Flask(__name__)

# connect to redis for storing logging info
r = helper_functions.connect_redis_db()

@app.route('/tweet_rate')
def tweet_rate():
    time_interval = float(request.args.get("time_interval"))
    r.ltrim('n_tweets',0,500) # only look at recent additions
    tweet_stats = [json.loads(s) for s in r.lrange('n_tweets', 0, -1)]
    df = pd.DataFrame(tweet_stats, columns=['time', 'n_tweet'])
    df_recent = df[time.time() - df['time'] < time_interval]
    rate = df_recent.n_tweet.sum()/float(time_interval)
    return str(rate)

@app.route('/avg_sentiment')
def compute_polarity():
    time_interval = float(request.args.get("time_interval"))
    r.ltrim('polarity',0,50)  # housekeeping; only look at recent additions
    tweet_stats = [json.loads(s) for s in r.lrange('polarity', 0, -1)]
    df = pd.DataFrame(tweet_stats, columns=['time', 'polarity'])
    df_recent = df[time.time() - df['time'] < time_interval]
    avg_polarity = df_recent.polarity.mean()
    if pd.isnull(avg_polarity):
        return str(0.5)
    return str(avg_polarity)


@app.route('/flushall')
def flushall():
    r.flushall()
    return "1"

@app.route('/getdata')
def getdata():
    return str(r.lrange('n_tweets', 0, -1))

# needed to make this application accessable for cross domain access
@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
  return response
