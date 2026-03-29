from apscheduler.schedulers.blocking import BlockingScheduler
from .jobs import registrar_jobs  # ← import relativo

scheduler = BlockingScheduler()
registrar_jobs(scheduler)

print("Scheduler iniciado. App Loger rodará a cada 20 minutos.")
scheduler.start()