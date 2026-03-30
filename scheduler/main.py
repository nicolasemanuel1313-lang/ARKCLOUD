from apscheduler.schedulers.blocking import BlockingScheduler
from .jobs import registrar_jobs  # ← import relativo

scheduler = BlockingScheduler()
registrar_jobs(scheduler)

print("Scheduler iniciado.")
scheduler.start()