import json
from pathlib import Path
from datetime import datetime, timedelta

CHECKIN_FILE = Path(__file__).parent / "checkin_log.json"


def _load_checkins():
    """Load all check-in records from the log file."""
    if not CHECKIN_FILE.exists():
        return []
    try:
        with open(CHECKIN_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def _save_checkins(checkins: list):
    """Save check-in records to the log file."""
    with open(CHECKIN_FILE, "w", encoding="utf-8") as f:
        json.dump(checkins, f, indent=2)


def get_current_status(username: str) -> dict:
    """Get the current check-in status for a user."""
    checkins = _load_checkins()
    
    # Find the most recent check-in/out for this user
    user_records = [c for c in checkins if c.get("username") == username]
    
    if not user_records:
        return {"status": "checked_out", "check_in_time": None}
    
    last_record = user_records[0]  # Most recent first
    return {
        "status": last_record.get("status", "checked_out"),
        "check_in_time": last_record.get("check_in_time"),
        "timestamp": last_record.get("timestamp")
    }


def calculate_duration(check_in_time_str: str) -> str:
    """Calculate duration from check-in time to now."""
    try:
        check_in_time = datetime.strptime(check_in_time_str, "%m/%d/%Y, %I:%M:%S %p")
        duration = datetime.now() - check_in_time
        hours = duration.seconds // 3600
        minutes = (duration.seconds % 3600) // 60
        return f"{hours} hour{'s' if hours != 1 else ''} and {minutes} minute{'s' if minutes != 1 else ''}"
    except:
        return "N/A"


def check_in(username: str):
    """Record a check-in for a user."""
    checkins = _load_checkins()
    timestamp = datetime.now().strftime("%m/%d/%Y, %I:%M:%S %p")
    
    record = {
        "username": username,
        "status": "checked_in",
        "check_in_time": timestamp,
        "timestamp": timestamp
    }
    
    checkins.insert(0, record)
    _save_checkins(checkins)


def check_out(username: str):
    """Record a check-out for a user."""
    checkins = _load_checkins()
    timestamp = datetime.now().strftime("%m/%d/%Y, %I:%M:%S %p")
    
    # Find the most recent check-in for this user
    user_records = [c for c in checkins if c.get("username") == username]
    if user_records and user_records[0].get("status") == "checked_in":
        check_in_time = user_records[0].get("check_in_time")
        duration = calculate_duration(check_in_time)
    else:
        duration = "N/A"
    
    record = {
        "username": username,
        "status": "checked_out",
        "check_in_time": None,
        "duration": duration,
        "timestamp": timestamp
    }
    
    checkins.insert(0, record)
    _save_checkins(checkins)


def get_history(username: str = None, limit: int = 5):
    """Get check-in/out history."""
    checkins = _load_checkins()
    
    if username:
        checkins = [c for c in checkins if c.get("username") == username]
    
    return checkins[:limit]
