from apps.app_loger.main import loger
from apps.app_report_previas.main import report
from datetime import datetime

def registrar_jobs(scheduler):
    scheduler.add_job(
        loger, # função main do app
        trigger="cron",
        minute="0,20,40",
        id="app_loger",
        #next_run_time=datetime.now() ,  # executa imediatamente ao subir
        name="App Loger - a cada 20 min",
        replace_existing=True
    )

    scheduler.add_job(
        report,
        trigger="cron",
        hour="7-23",       
        minute="10",        
        id="app_report_previas",
        name="Report Prévias - 1x por hora",
        replace_existing=True
    )