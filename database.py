import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect("office_audit.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS audit_logs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        session_id TEXT,
                        timestamp DATETIME,
                        app_title TEXT,
                        event_type TEXT,
                        screenshot_path TEXT)''')
    conn.commit()
    conn.close()

def log_event(session_id, app_title, event_type, ss_path):
    conn = sqlite3.connect("office_audit.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO audit_logs (session_id, timestamp, app_title, event_type, screenshot_path) VALUES (?,?,?,?,?)",
                   (session_id, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), app_title, event_type, ss_path))
    conn.commit()
    conn.close()

def get_session_history(session_id):
    conn = sqlite3.connect("office_audit.db")
    cursor = conn.cursor()
    cursor.execute("SELECT timestamp, app_title, event_type, screenshot_path FROM audit_logs WHERE session_id=?", (session_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows