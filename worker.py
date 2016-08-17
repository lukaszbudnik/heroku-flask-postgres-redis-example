import apscheduler.schedulers.blocking
import queue.queue

sched = apscheduler.schedulers.blocking.BlockingScheduler()

@sched.scheduled_job('interval', minutes=1)
def consume():
    try:
        data = queue.queue.consume()
    except Exception as e:
        # no, I'm not doing anything with the errors
        error_id=uuid.uuid1()

consume()

sched.start()
