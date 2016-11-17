from helper_functions import connect_redis_db

from rq import use_connection, Queue
import tasks

# Connect to Redis
conn = connect_redis_db()


# Offload the "myfunc" invocation
q = Queue(connection = conn)
q.enqueue(tasks.myfunc, 318, 62)
