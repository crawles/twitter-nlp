import json
import os
import time
import threading

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
        print 'THIS IS THE SERVICE:', json.loads(env_vars)
        credentials = json.loads(env_vars)[redis_service_name][0]['credentials']
        DB_HOST = credentials['host']
        DB_PORT = credentials['port']
        DB_PW = credentials['password']
        REDIS_DB = 0

    return redis.StrictRedis(host=DB_HOST,
                              port=DB_PORT,
                              password=DB_PW,
                              db=REDIS_DB)


def set_interval(func, sec):
    def func_wrapper():
        set_interval(func, sec)
        func()
    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t


def sse_pack(d):
    """For sending sse to client. Formats a dictionary into correct form for SSE"""
    buf = ''
    for k in ['retry','id','event','data']:
        if k in d.keys():
            buf += '{}: {}\n'.format(k, d[k])
    return buf + '\n'


def been_n_second(n,time_now,time_start,wait_time = 0.01):
    #TODO remove while loop and find better solution
    time_delta = time_now - time_start
    if time_delta >= n:
        return True
    # TODO remove time.sleep
    time.sleep(wait_time)
    return False
