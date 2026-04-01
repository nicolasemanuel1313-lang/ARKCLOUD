import traceback
from datetime import datetime, timezone
from functions.supabase_client import supabase

def log_execution(app_name, status, message=None, tb=None, started_at=None, finished_at=None):
    duration_ms = None
    if started_at and finished_at:
        duration_ms = int((finished_at - started_at).total_seconds() * 1000)

    supabase.table("LOGS").insert({
        "app_name": app_name,
        "status": status,
        "message": message,
        "traceback": tb,
        "started_at": started_at.isoformat() if started_at else None,
        "finished_at": finished_at.isoformat() if finished_at else None,
        "duration_ms": duration_ms,
    }).execute()