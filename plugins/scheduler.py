from apscheduler.scheduler import Scheduler

schedule_command = Scheduler()


@schedule_command.interval_schedule(seconds=10)
def some_job():
    print "Schedule Win"

schedule_command.start()