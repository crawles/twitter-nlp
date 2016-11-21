import datetime
import math
import random

import pandas as pd

from twitter_app import helper_functions

r = helper_functions.connect_redis_db()
r.lpush('n_tweets',(datetime.datetime.now(),math.floor(random.random() * 10)))
print r.lrange('n_tweets',0,-1)
print r.keys()

df = pd.DataFrame(r.lrange('n_tweets',0,-1))
print df

pd.to_msgpack(['hello','world'])