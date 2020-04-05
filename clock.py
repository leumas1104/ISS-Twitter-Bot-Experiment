import TwitterBot
from apscheduler.schedulers.blocking import BlockingScheduler

@sched.run_prog('interval', minutes=10)
def run_prog():
    TwitterBot.main()

sched.start()
    
    
    
