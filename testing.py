import helper_functions
import datetime
import random
import math
import pandas as pd

r = helper_functions.connect_redis_db()
r.lpush('n_tweets',(datetime.datetime.now(),math.floor(random.random() * 10)))
print r.lrange('n_tweets',0,-1)
print r.keys()

df = pd.DataFrame(r.lrange('n_tweets',0,-1))
print df

pd.to_msgpack(['hello','world'])