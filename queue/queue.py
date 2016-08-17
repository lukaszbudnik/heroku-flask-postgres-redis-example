import os
import redis
import os
import psycopg2
import urlparse

urlparse.uses_netloc.append("postgres")

def create_db_connection():
    url = urlparse.urlparse(os.environ["DATABASE_URL"])
    conn = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )
    return conn

def create_redis_connecton():
    url = os.environ.get("REDIS_URL")
    r = redis.from_url(url)
    return r

def publish(data):
    with create_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT nextval('queue_id_seq')")
            seq = cur.fetchone()
            (id,) = seq
            cur.execute("INSERT INTO queue (id, data) VALUES (%s, %s)", (id, data))
            conn.commit()
            increment_queue_size()
            return id

def consume():
    with create_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM queue")
            record = cur.fetchone()
            if record is None:
                return
            id, data = record
            cur.execute("DELETE FROM queue WHERE id = %s", (id,))
            conn.commit()
            decrement_queue_size()
            return data

def get_queue_size_db():
    with create_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT count(*) from queue")
            count = cur.fetchone()
            (queue_size,) = count
            # if queue is empty, cursor is empty, return 0
            if queue_size is None:
                return 0
            return queue_size

def get_queue_size(put_to_cache = False):
    redis = create_redis_connecton()
    queue_size = redis.get('queue_size')
    source = None

    if queue_size is None:
        # if redis doesn't have queue size get it straight from the queue
        queue_size = get_queue_size_db()
        source = 'db'
        if put_to_cache:
            redis.set('queue_size', queue_size, ex = 10)
    else:
        # if redis has queue size just convert it to int
        queue_size = int(queue_size)
        source = 'redis'

    return queue_size, source

def increment_queue_size():
    queue_size, source = get_queue_size()

    # if source is redis, increment it
    # if source is db then the queue_size is the actual count returned
    if source == 'redis':
        queue_size = queue_size + 1

    redis = create_redis_connecton()
    # expire every 10 seconds
    redis.set('queue_size', queue_size, ex = 10)

def decrement_queue_size():
    queue_size, source = get_queue_size()

    # if source is redis, increment it
    # if source is db then the queue_size is the actual count returned
    if source == 'redis':
        queue_size = queue_size - 1

    redis = create_redis_connecton()
    # expire every 10 seconds
    redis.set('queue_size', queue_size, ex = 10)
