import json
import hashlib
from pathlib import Path
from datetime import datetime, timedelta

USERS_FILE = Path(__file__).parent / "users.json"
LOGIN_ATTEMPTS_FILE = Path(__file__).parent / "data" / "login_attempts.json"
# Lockout policy
MAX_FAILED_ATTEMPTS = 3
LOCKOUT_MINUTES = 15


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


def _load_login_attempts():
    """Load failed login attempts tracking."""
    if not LOGIN_ATTEMPTS_FILE.exists():
        return {}
    try:
        with open(LOGIN_ATTEMPTS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def _save_login_attempts(attempts: dict):
    """Save failed login attempts tracking."""
    LOGIN_ATTEMPTS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(LOGIN_ATTEMPTS_FILE, "w", encoding="utf-8") as f:
        json.dump(attempts, f, indent=2)


def _hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def _is_account_locked(username: str) -> tuple:
    """Check if account is locked due to failed attempts.
    Returns (is_locked, remaining_minutes)"""
    attempts = _load_login_attempts()
    key = username.strip().lower()
    
    if key not in attempts:
        return False, 0
    
    attempt_data = attempts[key]
    failed_count = attempt_data.get("failed_count", 0)
    
    if failed_count < MAX_FAILED_ATTEMPTS:
        return False, 0
    
    # Check if lockout period has expired (15 minutes)
    last_attempt_str = attempt_data.get("last_attempt_time", "")
    if last_attempt_str:
        try:
            last_attempt = datetime.fromisoformat(last_attempt_str)
            lockout_time = last_attempt + timedelta(minutes=LOCKOUT_MINUTES)
            now = datetime.now()
            
            if now < lockout_time:
                remaining = (lockout_time - now).total_seconds() / 60
                return True, int(remaining) + 1
            else:
                # Lockout period expired, reset attempts
                attempts[key] = {
                    "failed_count": 0,
                    "last_attempt_time": "",
                    "locked_at": ""
                }
                _save_login_attempts(attempts)
                return False, 0
        except Exception:
            pass
    
    return False, 0


def _record_failed_attempt(username: str):
    """Record a failed login attempt."""
    attempts = _load_login_attempts()
    key = username.strip().lower()
    
    if key not in attempts:
        attempts[key] = {
            "failed_count": 0,
            "last_attempt_time": "",
            "locked_at": ""
        }
    
    attempts[key]["failed_count"] = attempts[key].get("failed_count", 0) + 1
    attempts[key]["last_attempt_time"] = datetime.now().isoformat()
    
    # Set locked_at timestamp if just reached MAX_FAILED_ATTEMPTS
    if attempts[key]["failed_count"] == MAX_FAILED_ATTEMPTS:
        attempts[key]["locked_at"] = datetime.now().isoformat()
    
    _save_login_attempts(attempts)


def _reset_login_attempts(username: str):
    """Reset failed login attempts on successful login."""
    attempts = _load_login_attempts()
    key = username.strip().lower()
    
    if key in attempts:
        attempts[key] = {
            "failed_count": 0,
            "last_attempt_time": "",
            "locked_at": ""
        }
        _save_login_attempts(attempts)


def get_login_attempts(username: str) -> dict:
    """Get login attempt information for a user."""
    attempts = _load_login_attempts()
    key = username.strip().lower()
    
    if key not in attempts:
        return {
            "failed_count": 0,
            "last_attempt_time": "",
            "locked_at": ""
        }
    
    return attempts[key]


def add_user(username: str, password: str, email: str = None) -> bool:
    """Add a user. Returns True if created, False if user exists.
    Username is normalized (stripped, lowercased) for consistency."""
    users = _load_users()
    key = username.strip().lower()
    if key in users:
        return False
    users[key] = {
        "password_hash": _hash_password(password)
    }
    if email:
        users[key]["email"] = email.strip()
    _save_users(users)
    return True


def check_credentials(username: str, password: str) -> tuple:
    """Check login credentials.
    Returns (success: bool, message: str, remaining_lockout_time: int)"""
    key = username.strip().lower()

    users = _load_users()
    if key not in users:
        _record_failed_attempt(key)
        attempts = _load_login_attempts()
        failed_count = attempts.get(key, {}).get("failed_count", 1)
        return False, f"Invalid username or password. Attempt {failed_count}/{MAX_FAILED_ATTEMPTS}", 0

    # Admin/user manual lock
    if users[key].get("locked"):
        return False, "Account locked by admin. Contact administrator.", 0

    # Check lockout from failed attempts
    is_locked, remaining_minutes = _is_account_locked(key)
    if is_locked:
        return False, f"Account locked. Try again in {remaining_minutes} minutes.", remaining_minutes
    
    if users[key].get("password_hash") != _hash_password(password):
        _record_failed_attempt(key)
        attempts = _load_login_attempts()
        failed_count = attempts.get(key, {}).get("failed_count", 1)
        return False, f"Invalid username or password. Attempt {failed_count}/{MAX_FAILED_ATTEMPTS}", 0
    
    # Credentials valid - reset attempts
    _reset_login_attempts(key)
    return True, "Login successful", 0


def list_users() -> list:
    users = _load_users()
    return list(users.keys())
