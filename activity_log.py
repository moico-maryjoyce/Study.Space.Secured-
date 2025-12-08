import json
from pathlib import Path
from datetime import datetime

ACTIVITY_FILE = Path(__file__).parent / "data" / "activity_log.json"


def _load_activities():
    """Load all activities from the log file."""
    if not ACTIVITY_FILE.exists():
        return []
    try:
        with open(ACTIVITY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def _save_activities(activities: list):
    """Save activities to the log file."""
    # Ensure data directory exists
    ACTIVITY_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(ACTIVITY_FILE, "w", encoding="utf-8") as f:
        json.dump(activities, f, indent=2)


def log_activity(event_type: str, username: str, description: str):
    """Log a new activity."""
    activities = _load_activities()
    timestamp = datetime.now().strftime("%m/%d/%Y, %I:%M:%S %p")
    
    activity = {
        "event_type": event_type,
        "username": username,
        "timestamp": timestamp,
        "description": description
    }
    
    # Add to the beginning (most recent first)
    activities.insert(0, activity)
    
    # Keep only the last 100 activities
    activities = activities[:100]
    
    _save_activities(activities)


def get_recent_activities(limit: int = 5):
    """Get the most recent activities."""
    activities = _load_activities()
    return activities[:limit]
