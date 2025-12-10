import json
import mysql.connector
from pathlib import Path
from datetime import datetime

# 1. Import the connection function from your db.py
from db import get_connection

def load_json_file(path):
    file_path = Path(__file__).parent / path
    if not file_path.exists():
        print(f"Warning: {path} not found.")
        return []
    return json.loads(file_path.read_text(encoding='utf-8'))

def insert_users(conn, users):
    cur = conn.cursor()
    
    # Handle the dictionary-of-dictionaries format in users.json
    if isinstance(users, dict):
        users_list = []
        for username, user_data in users.items():
            if isinstance(user_data, dict):
                user_data['username'] = username
                users_list.append(user_data)
        users = users_list
    
    print(f"Importing {len(users)} users...")
    
    for u in users:
        if not isinstance(u, dict):
            continue

        # Extract fields matching your database.py schema
        username = u.get('username') or u.get('user')
        # Fallback if name is missing
        name = u.get('name') or username
        email = u.get('email') or f"{username}@example.com"
        password_hash = u.get('password_hash') or ''
        role = u.get('role', 'User')
        status = u.get('status', 'Active')
        locked = 1 if u.get('locked') else 0
        twofa = 1 if u.get('twofa') else 0
        last_login = u.get('last_login') or None

        # 2. Updated Query: Matches schema in database.py (uses 'role' string, not 'role_id')
        try:
            cur.execute("""
                INSERT INTO users 
                (username, name, email, role, locked, twofa, status, last_login, password_hash)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                name=VALUES(name), email=VALUES(email), role=VALUES(role), 
                last_login=VALUES(last_login), password_hash=VALUES(password_hash)
            """, (username, name, email, role, locked, twofa, status, last_login, password_hash))
        except mysql.connector.Error as err:
            print(f"Error inserting user {username}: {err}")

    conn.commit()

def insert_checkins(conn, checkins):
    cur = conn.cursor()
    if not isinstance(checkins, list):
        checkins = []
        
    print(f"Importing {len(checkins)} check-in records...")

    for c in checkins:
        if not isinstance(c, dict):
            continue
            
        username = c.get('username') or c.get('user')
        checkin_time = c.get('check_in_time') or c.get('timestamp')
        
        # 3. Updated Query: Matches schema (uses 'username', not 'user_id')
        # Note: Your checkin_logs table creates columns for checkin_time/checkout_time
        # but your JSON sometimes has just 'timestamp'. We map accordingly.
        try:
            cur.execute("""
                INSERT INTO checkin_logs (username, checkin_time, note)
                VALUES (%s, %s, %s)
            """, (username, checkin_time, "Imported from JSON"))
        except mysql.connector.Error as err:
            print(f"Error inserting checkin: {err}")

    conn.commit()

def insert_activities(conn, activities):
    cur = conn.cursor()
    if not isinstance(activities, list):
        activities = []
        
    print(f"Importing {len(activities)} activity logs...")

    for a in activities:
        if not isinstance(a, dict):
            continue
            
        username = a.get('username') or a.get('user')
        event_type = a.get('event_type') or a.get('action')
        timestamp = a.get('timestamp')
        description = a.get('description')
        
        # 4. Updated Query: Matches schema (uses 'event_type' and 'username')
        try:
            cur.execute("""
                INSERT INTO activity_logs (event_type, username, timestamp, description)
                VALUES (%s, %s, %s, %s)
            """, (event_type, username, timestamp, description))
        except mysql.connector.Error as err:
            print(f"Error inserting activity: {err}")

    conn.commit()

def main():
    # 5. Use the connection from db.py
    print("Connecting to database via db.py...")
    try:
        conn = get_connection()
        print("Connected successfully.")
        
        users = load_json_file('data/users.json')
        checkins = load_json_file('data/checkin_log.json')
        activities = load_json_file('data/activity_log.json')

        insert_users(conn, users)
        insert_checkins(conn, checkins)
        insert_activities(conn, activities)
        
        print("Data import completed.")
        conn.close()
    except Exception as e:
        print(f"Critical Error: {e}")

if __name__ == '__main__':
    main()
