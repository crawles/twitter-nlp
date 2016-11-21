import json
import os
import time

import redis

# initialize redis connection for local and CF deployment
def connect_redis_db(redis_service_name = 'p-redis'):
    if os.environ.get('VCAP_SERVICES') is None: # running locally
        DB_HOST = 'localhost'
        DB_PORT = 6379
        DB_PW = ''
        REDIS_DB = 1
    else:                                       # running on CF
        env_vars = os.environ['VCAP_SERVICES']
        credentials = json.loads(env_vars)[redis_service_name][0]['credentials']
        DB_HOST = credentials['host']
        DB_PORT = credentials['port']
        DB_PW = credentials['password']
        REDIS_DB = 0

    return redis.StrictRedis(host=DB_HOST,
                              port=DB_PORT,
                              password=DB_PW,
                              db=REDIS_DB)


def been_n_second(n,time_now,time_start,wait_time = 0.01):
    time_delta = time_now - time_start
    if time_delta >= n:
        return True
    time.sleep(wait_time)
    return False