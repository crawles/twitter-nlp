import os

from flask import Flask
from gevent.pywsgi import WSGIServer

import helper_functions

r = helper_functions.connect_redis_db()

app = Flask(__name__)

@app.route('/')
def view_tweets():
    pubsub = r.pubsub()
    pubsub.subscribe('tweet_msgs')
    for msg in pubsub.listen():
        if msg['type'] == 'message':
            break
    pubsub.unsubscribe()
    return str(msg)

if __name__ == '__main__':
    if os.environ.get('VCAP_SERVICES') is None: # running locally
        PORT = 8080
    else:                                       # running on CF
        PORT = int(os.getenv("PORT"))
    http_server = WSGIServer(('0.0.0.0',PORT), app)
    http_server.serve_forever()
