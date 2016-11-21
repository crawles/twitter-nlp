# -*- coding: utf-8 -*-

'''
sentiment_service.py
~~~~~~~~~~~~~~~~~~~~

App implements a sentiment analysis pipeline. 

'''

import cPickle
import json
import os
import time

from flask import Flask, request, jsonify
import pandas as pd
import redis
import requests
import sklearn

import helper_functions

resp = requests.get("https://raw.githubusercontent.com/crawles/gpdb_sentiment_analysis_twitter_model/master/twitter_sentiment_model.pkl")
resp.raise_for_status()
cl = cPickle.loads(resp.content)

# connect to redis for storing logging info
r = helper_functions.connect_redis_db()

# init tweet counter
r['tweet_counter'] = 0

def regex_preprocess(raw_tweets):
    pp_text = pd.Series(raw_tweets)
    
    user_pat = '(?<=^|(?<=[^a-zA-Z0-9-_\.]))@([A-Za-z]+[A-Za-z0-9]+)'
    http_pat = '(https?:\/\/(?:www\.|(?!www))[^\s\.]+\.[^\s]{2,}|www\.[^\s]+\.[^\s]{2,})'
    repeat_pat, repeat_repl = "(.)\\1\\1+",'\\1\\1'

    pp_text = pp_text.str.replace(pat = user_pat, repl = 'USERNAME')
    pp_text = pp_text.str.replace(pat = http_pat, repl = 'URL')
    pp_text.str.replace(pat = repeat_pat, repl = repeat_repl)
    return pp_text

app = Flask(__name__)

@app.route('/polarity_compute', methods=['POST','OPTIONS'])
@helper_functions.crossdomain(origin='*')
def sentiment_compute():
    req = request.get_json(force=True)
    print request.get_json()
    X = regex_preprocess(req['data'])
    prediction = cl.predict_proba(X)[:][:,1]

    # for logging
    tweet_packet = {'time': time.time(),'n_tweet':len(X)}
    r.lpush('n_tweets',json.dumps(tweet_packet))
    r['tweet_counter'] = int(r['tweet_counter']) + len(X)

    return(jsonify({"polarity" : prediction.tolist()}))


if __name__ == "__main__":
    if os.environ.get('VCAP_SERVICES') is None: # running locally
        PORT = 5000
        DEBUG = True
        app.run(debug=DEBUG)
    else:                                       # running on CF
        PORT = int(os.getenv("PORT"))
        DEBUG = False
        app.run(host='0.0.0.0', port=PORT, debug=DEBUG)

