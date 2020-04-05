import TwitterBot
from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()
@sched.scheduled_job('interval', minutes=10)
def timed_job():
    TwitterBot.TwitterBot()

sched.start()
    
    
    
