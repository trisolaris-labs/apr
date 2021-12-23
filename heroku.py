from apr import apr
from apscheduler.schedulers.blocking import BlockingScheduler

# Create an instance of scheduler and add function.
scheduler = BlockingScheduler()
scheduler.add_job(apr, "interval", seconds=120)

scheduler.start()