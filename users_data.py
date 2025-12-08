import json
from pathlib import Path
from datetime import datetime
from activity_log import log_activity

USERS_FILE = Path(__file__).parent / "users.json"


def _load_users():
    if not USERS_FILE.exists():
        return {}
    try:
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def _save_users(users: dict):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=2)


def list_users():
    users = _load_users()
    # Return list of dicts with normalized fields
    out = []
    for username, data in users.items():
        out.append({
            "username": username,
            "name": data.get("name", ""),
            "email": data.get("email", ""),
            "role": data.get("role", "User"),
            "status": data.get("status", "Active"),
            "twofa": data.get("twofa", False),
            "last_login": data.get("last_login", ""),
            "locked": data.get("locked", False),
        })
    # Most recent first by default if stored ordering exists
    return out


def get_user(username: str):
    users = _load_users()
    return users.get(username.strip().lower())


def delete_user(username: str, actor: str = "system") -> bool:
    users = _load_users()
    key = username.strip().lower()
    if key not in users:
        return False
    users.pop(key)
    _save_users(users)
    log_activity("user_deleted", actor, f"User {username} deleted by {actor}")
    return True


def toggle_lock(username: str, actor: str = "system") -> bool:
    users = _load_users()
    key = username.strip().lower()
    if key not in users:
        return False
    users[key]["locked"] = not users[key].get("locked", False)
    status = "locked" if users[key]["locked"] else "unlocked"
    _save_users(users)
    log_activity("user_locked" if users[key]["locked"] else "user_unlocked", actor, f"User {username} {status} by {actor}")
    return True


def add_user_record(username: str, name: str = "", email: str = "", role: str = "User") -> bool:
    users = _load_users()
    key = username.strip().lower()
    
    # Update existing user with additional metadata
    if key in users:
        users[key]["name"] = name
        users[key]["email"] = email
        users[key]["role"] = role
        users[key]["status"] = "Active"
        users[key]["twofa"] = False
        users[key]["last_login"] = ""
        users[key]["locked"] = False
        _save_users(users)
        return True
    
    # Create new user if doesn't exist
    users[key] = {
        "name": name,
        "email": email,
        "role": role,
        "status": "Active",
        "twofa": False,
        "last_login": "",
        "locked": False
    }
    _save_users(users)
    log_activity("user_created", "admin", f"New user {username} created with email {email}")
    return True


def search_users(role: str = None, status: str = None, query: str = None):
    users = list_users()
    results = users
    if role and role != "All Roles":
        results = [u for u in results if u.get("role") == role]
    if status and status != "All Status":
        results = [u for u in results if u.get("status") == status]
    if query:
        q = query.strip().lower()
        results = [u for u in results if q in u.get("username", "").lower() or q in u.get("email", "").lower() or q in u.get("name", "").lower()]
    return results
