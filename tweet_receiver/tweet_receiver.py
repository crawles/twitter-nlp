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
    http_server = WSGIServer(('',5000), app)
    http_server.serve_forever()