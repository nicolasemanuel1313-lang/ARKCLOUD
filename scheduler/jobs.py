import threading
from apps.app_loger.main import loger
from apps.app_report_previas.main import report
from apps.app_loger_212.main import loger_212


def com_timeout(func, timeout_seg: int):
    """Executa func em thread separada com timeout máximo em segundos."""
    def wrapper():
        erro = [None]

        def _run():
            try:
                func()
            except Exception as e:
                erro[0] = e

        t = threading.Thread(target=_run, daemon=True)
        t.start()
        t.join(timeout=timeout_seg)

        if t.is_alive():
            raise TimeoutError(
                f"⏰ [{func.__name__}] travou — abortado após {timeout_seg}s"
            )

        if erro[0]:
            raise erro[0]

    wrapper.__name__ = func.__name__
    return wrapper


def registrar_jobs(scheduler):
    jobs = [
        {
            "func":        loger,
            "timeout_seg": 900,   # 15 min — executa a cada 20 min
            "trigger":     "cron",
            "kwargs":      {"minute": "0,20,40"},
            "id":          "app_loger",
            "name":        "App Loger 29 - a cada 20 min",
        },
        {
            "func":        report,
            "timeout_seg": 300,   # 5 min — executa 1x por hora
            "trigger":     "cron",
            "kwargs":      {"hour": "7-20", "minute": "10"},
            "id":          "app_report_previas",
            "name":        "Report Prévias - 1x por hora",
        },
        {
            "func":        loger_212,
            "timeout_seg": 900,   
            "trigger":     "cron",
            "kwargs":      {"minute": "5,25,45"},
            "id":          "app_loger_212",
            "name":        "App Loger 212 - a cada 20 min",
        }
    ]

    for job in jobs:
        scheduler.add_job(
            com_timeout(job["func"], job["timeout_seg"]),
            trigger=job["trigger"],
            id=job["id"],
            name=job["name"],
            replace_existing=True,
            **job["kwargs"]
        )