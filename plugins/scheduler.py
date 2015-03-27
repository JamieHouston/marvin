import asyncio
from datetime import datetime, timedelta
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.redis import RedisJobStore

def some_job():
    print("Time for standup")


def do_the_work():
    scheduler = AsyncIOScheduler()
    # scheduler.store = RedisJobStore(
    #     db=0,
    #     jobs_key='marvin:scheduler:jobs',
    #     run_times_key="marvin:scheduler:runtimes",
    #     args={'host': 'pub-redis-10118.us-east-1-2.4.ec2.garantiadata.com', 'port':10118,
    #     'password': "P@ssw0rd"})

    standup_time = datetime.now() + timedelta(seconds=5)

    scheduler.add_job(some_job, 'date', next_run_time=standup_time)

    scheduler.start()

if __name__ == '__main__':
    do_the_work()

    try:
        asyncio.get_event_loop().run_forever()
    except(KeyboardInterrupt, SystemExit):
        pass