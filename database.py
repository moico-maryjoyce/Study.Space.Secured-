"""MySQL database helper and initializer for the app.

Usage:
    python database.py

This will connect to the MySQL database and create tables,
and optionally import JSON data found in the `data/` folder.
"""
import mysql.connector
from mysql.connector import Error
import os
import json
from typing import List

# MySQL connection configuration
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "study_space_secured_db",
    "port": 3306
}


def get_connection():
    """Return a MySQL connection."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        raise


def init_db(conn):
    """Create required tables if they don't exist."""
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(255) UNIQUE,
        name VARCHAR(255),
        email VARCHAR(255),
        role VARCHAR(50),
        locked INT DEFAULT 0,
        twofa INT DEFAULT 0,
        status VARCHAR(50),
        last_login DATETIME,
        password_hash VARCHAR(255)
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS activity_logs (
        id INT AUTO_INCREMENT PRIMARY KEY,
        event_type VARCHAR(100),
        username VARCHAR(255),
        timestamp DATETIME,
        description TEXT,
        ip_address VARCHAR(50)
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS checkin_logs (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(255),
        checkin_time DATETIME,
        checkout_time DATETIME,
        note TEXT
    )
    """)

    conn.commit()


def import_json_to_db(conn, data_dir: str = None):
    """Import JSON files from `data/` into the DB tables (best-effort)."""
    root = os.path.dirname(__file__)
    data_dir = data_dir or os.path.join(root, "data")

    # users.json
    users_path = os.path.join(data_dir, "users.json")
    if os.path.exists(users_path):
        with open(users_path, "r", encoding="utf-8") as f:
            users = json.load(f)
        # Normalize dict-of-dicts to list
        if isinstance(users, dict):
            users = [
                {"username": uname, **udata} if isinstance(udata, dict) else {"username": uname}
                for uname, udata in users.items()
            ]
        cur = conn.cursor()
        for u in users:
            cur.execute(
                """INSERT IGNORE INTO users (username, name, email, role, locked, twofa, status, last_login)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                (
                    u.get("username"),
                    u.get("name"),
                    u.get("email"),
                    u.get("role"),
                    1 if u.get("locked") else 0,
                    1 if u.get("twofa") else 0,
                    u.get("status"),
                    u.get("last_login"),
                ),
            )
        conn.commit()

    # activity_log.json
    activity_path = os.path.join(data_dir, "activity_log.json")
    if os.path.exists(activity_path):
        with open(activity_path, "r", encoding="utf-8") as f:
            logs = json.load(f)
        cur = conn.cursor()
        for l in logs:
            cur.execute(
                """INSERT INTO activity_logs (event_type, username, timestamp, description, ip_address)
                VALUES (%s, %s, %s, %s, %s)""",
                (
                    l.get("event_type"),
                    l.get("username") or l.get("user"),
                    l.get("timestamp"),
                    l.get("description"),
                    l.get("ip_address"),
                ),
            )
        conn.commit()

    # checkin_log.json (best effort)
    checkin_path = os.path.join(data_dir, "checkin_log.json")
    if os.path.exists(checkin_path):
        with open(checkin_path, "r", encoding="utf-8") as f:
            checks = json.load(f)
        cur = conn.cursor()
        for c in checks:
            cur.execute(
                """INSERT INTO checkin_logs (username, checkin_time, checkout_time, note)
                VALUES (%s, %s, %s, %s)""",
                (
                    c.get("username") or c.get("user"),
                    c.get("checkin_time") or c.get("timestamp"),
                    c.get("checkout_time"),
                    c.get("note") or c.get("action") or "",
                ),
            )
        conn.commit()


def list_tables(conn) -> List[str]:
    cur = conn.cursor()
    cur.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = %s", (DB_CONFIG["database"],))
    return [r[0] for r in cur.fetchall()]


if __name__ == "__main__":
    print("Initializing MySQL DB:", DB_CONFIG["database"])
    conn = get_connection()
    init_db(conn)
    import_json_to_db(conn)
    print("Done. Tables:", list_tables(conn))
    conn.close()
