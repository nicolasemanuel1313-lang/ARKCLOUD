from apscheduler.schedulers.blocking import BlockingScheduler
from .jobs import registrar_jobs

scheduler = BlockingScheduler()
registrar_jobs(scheduler)

print("Arkcloud - iniciado.")
scheduler.start()