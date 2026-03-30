from apps.app_loger.main import loger
from datetime import datetime

def registrar_jobs(scheduler):
    scheduler.add_job(
        loger, # função main do app
        trigger="cron",
        minutes="0,20,40",
        id="app_loger",
        #next_run_time=datetime.now() ,  # executa imediatamente ao subir
        name="App Loger - a cada 20 min",
        replace_existing=True
    )