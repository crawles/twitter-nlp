import json
import os
import time

import redis
from flask import Flask, request, Response, render_template
from gevent import monkey, sleep, socket
from gevent.pywsgi import WSGIServer

import helper_functions

monkey.patch_all()

app = Flask(__name__)
redis.connection.socket = socket

# connect to redis for storing logging info
r = helper_functions.connect_redis_db()


def gen_dashboard_tweets():
    n = 5  # min number of seconds between each tweet
    pubsub = r.pubsub()
    pubsub.subscribe('tweet_msgs')
    for message in pubsub.listen():
        is_a_tweet = message['type'] == 'message'
        is_tweet_message = message['channel'] == 'tweet_msgs'
        if not is_a_tweet or not is_tweet_message:
            continue
        msg = json.loads(message['data'])
        tweet_sent = {"data": json.dumps({"tweet": msg['text'],
                                          "polarity": '{:1.2f}'.format(msg['polarity'])})}
        yield (helper_functions.sse_pack(tweet_sent))
        sleep(n-2) # new tweet won't get published for n seconds, let python rest


def get_tweet_stats():
    pubsub = r.pubsub()
    pubsub.subscribe('tweet_stats')
    for message in pubsub.listen():
        time_start = time.time()
        is_a_tweet = message['type'] == 'message'
        is_a_tweet_stat = message['channel'] == 'tweet_stats'
        if not is_a_tweet or not is_a_tweet_stat:
            continue
        tweet_stats = json.loads(message['data'])
        time_start = time.time()
        yield helper_functions.sse_pack({"data": json.dumps({"tweetRate": tweet_stats['tweet_rate'],
                                                             "avgPolarity": tweet_stats['avg_polarity']})})

@app.route('/live_tweets')
def live_tweets_sse():
    return Response(gen_dashboard_tweets(),mimetype='text/event-stream')

@app.route('/tweet_rate')
def tweet_rate_sse():
    return Response(get_tweet_stats(),mimetype='text/event-stream')

#TODO:is this depreicated?
@app.route('/swarm', methods=["POST"])
def swarm():
    print request.url
    assert request.method == "POST"

    locust_count = int(request.form["locust_count"])
    hatch_rate = float(request.form["hatch_rate"])
    return "True"

@app.route('/')
def page():
    return render_template('index.html')

if __name__ == '__main__':
    if os.environ.get('VCAP_SERVICES') is None: # running locally
        PORT = 5001
        app.debug = True
    else:                                       # running on CF
        PORT = int(os.getenv("PORT"))
    http_server = WSGIServer(('0.0.0.0',PORT), app)
    http_server.serve_forever()