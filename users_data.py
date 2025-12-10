import json
from pathlib import Path
from datetime import datetime
from activity_log import log_activity
import hashlib
from auth import _reset_login_attempts


def _delete_user_from_db(username: str) -> bool:
    """Best-effort delete from MySQL users table."""
    try:
        from db import get_connection
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM users WHERE username = %s", (username,))
        conn.commit()
        cur.close()
        conn.close()
        return True
    except Exception:
        return False


def _write_user_to_db(username: str, user_rec: dict) -> bool:
    """
    Best-effort write to MySQL users table.
    If the DB or connector is unavailable, fail silently.
    """
    try:
        from db import get_connection
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO users (username, name, email, role, locked, twofa, status, last_login, password_hash)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                name=VALUES(name),
                email=VALUES(email),
                role=VALUES(role),
                locked=VALUES(locked),
                twofa=VALUES(twofa),
                status=VALUES(status),
                last_login=VALUES(last_login),
                password_hash=VALUES(password_hash)
            """,
            (
                username,
                user_rec.get("name"),
                user_rec.get("email"),
                user_rec.get("role", "User"),
                1 if user_rec.get("locked") else 0,
                1 if user_rec.get("twofa") else 0,
                user_rec.get("status", "Active"),
                user_rec.get("last_login") or None,
                user_rec.get("password_hash"),
            ),
        )
        conn.commit()
        cur.close()
        conn.close()
        return True
    except Exception:
        return False

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
    key = username.strip().lower()
    json_deleted = False
    db_deleted = False

    # Delete in JSON
    try:
        users = _load_users()
        if key in users:
            users.pop(key)
            _save_users(users)
            json_deleted = True
    except Exception:
        json_deleted = False

    # Delete in DB (best effort)
    db_deleted = _delete_user_from_db(key)

    if json_deleted or db_deleted:
        log_activity("user_deleted", actor, f"User {username} deleted by {actor}")
        return True
    return False


def toggle_lock(username: str, actor: str = "system") -> bool:
    users = _load_users()
    key = username.strip().lower()
    if key not in users:
        return False
    users[key]["locked"] = not users[key].get("locked", False)
    status = "locked" if users[key]["locked"] else "unlocked"
    _save_users(users)
    # Clear failed attempts on unlock
    if not users[key]["locked"]:
        try:
            _reset_login_attempts(key)
        except Exception:
            pass
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
        _write_user_to_db(key, users[key])
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
    _write_user_to_db(key, users[key])
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


def ensure_default_admin_user():
    """
    Guarantee a baseline admin account exists and is usable.
    - Ensures `admin` user exists with password `Admin@123`
    - Unlocks the account and clears lockout attempts
    """
    users = _load_users()
    default_password_hash = hashlib.sha256("Admin@123".encode("utf-8")).hexdigest()
    admin = users.get("admin", {})

    # Apply/override required fields
    admin["password_hash"] = default_password_hash
    admin["name"] = admin.get("name") or "Administrator"
    admin["email"] = admin.get("email") or "admin@example.com"
    admin["role"] = "Admin"
    admin["status"] = "Active"
    admin["twofa"] = admin.get("twofa", False)
    admin["last_login"] = admin.get("last_login", "")
    admin["locked"] = False  # ensure unlocked

    users["admin"] = admin
    _save_users(users)

    # Clear lockout attempts for admin
    try:
        _reset_login_attempts("admin")
    except Exception:
        pass

    # Log only when we had to create missing admin
    if admin.get("name") == "Administrator" and not admin.get("last_login"):
        log_activity("user_created", "system", "Default admin account ensured")
