import sqlite3
from datetime import datetime

DATABASE = "logs_system.db"

def initialize_system():
    conn = sqlite3.connect(DATABASE)
    conn.execute("PRAGMA foreign_keys = 1")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS EventSources (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            location TEXT,
            type TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS EventTypes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type_name TEXT UNIQUE,
            severity TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS SecurityEvents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME,
            source_id INTEGER,
            event_type_id INTEGER,
            message TEXT,
            ip_address TEXT,
            username TEXT,
            FOREIGN KEY (source_id) REFERENCES EventSources(id),
            FOREIGN KEY (event_type_id) REFERENCES EventTypes(id)
        )
    """)

    conn.commit()
    conn.close()

def register_source(name, location, src_type):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO EventSources (name, location, type) VALUES (?, ?, ?)", 
                       (name, location, src_type))
        conn.commit()
    except sqlite3.IntegrityError:
        pass
    finally:
        conn.close()

def register_event_type(name, severity):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO EventTypes (type_name, severity) VALUES (?, ?)", 
                       (name, severity))
        conn.commit()
    except sqlite3.IntegrityError:
        pass
    finally:
        conn.close()

def log_security_event(source, event_type, message, ip=None, user=None):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM EventSources WHERE name = ?", (source,))
    src_row = cursor.fetchone()

    cursor.execute("SELECT id FROM EventTypes WHERE type_name = ?", (event_type,))
    type_row = cursor.fetchone()

    if src_row and type_row:
        current_time = datetime.now()
        cursor.execute("""
            INSERT INTO SecurityEvents (timestamp, source_id, event_type_id, message, ip_address, username)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (current_time, src_row[0], type_row[0], message, ip, user))
        conn.commit()
    else:
        print(f"[Error] Could not log event: Source '{source}' or Type '{event_type}' unknown.")
    
    conn.close()

def get_failed_logins_24h():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT s.timestamp, s.username, s.ip_address 
        FROM SecurityEvents s
        JOIN EventTypes t ON s.event_type_id = t.id
        WHERE t.type_name = 'Login Failed' 
        AND s.timestamp > datetime('now', '-1 day')
    """)
    data = cursor.fetchall()
    
    print(f"\n--- Recent Failed Logins (24h): {len(data)} found ---")
    for row in data:
        print(f"Time: {row[0]} | User: {row[1]} | IP: {row[2]}")
    conn.close()

def analyze_brute_force():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT s.ip_address, COUNT(*) 
        FROM SecurityEvents s
        JOIN EventTypes t ON s.event_type_id = t.id
        WHERE t.type_name = 'Login Failed' 
        AND s.timestamp > datetime('now', '-1 hour')
        GROUP BY s.ip_address
        HAVING COUNT(*) > 5
    """)
    data = cursor.fetchall()
    
    print("\n--- Potential Brute Force Attacks ---")
    if not data:
        print("System secure. No anomalies detected.")
    else:
        for row in data:
            print(f"[ALERT] IP {row[0]} triggered {row[1]} failed attempts in the last hour!")
    conn.close()

def report_critical_events():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT src.name, COUNT(*) 
        FROM SecurityEvents s
        JOIN EventTypes t ON s.event_type_id = t.id
        JOIN EventSources src ON s.source_id = src.id
        WHERE t.severity = 'Critical' 
        AND s.timestamp > datetime('now', '-7 days')
        GROUP BY src.name
    """)
    data = cursor.fetchall()
    
    print("\n--- Critical Events Report (Weekly) ---")
    for row in data:
        print(f"Source: {row[0]} -> {row[1]} critical events")
    conn.close()

def search_messages(keyword):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    cursor.execute("SELECT timestamp, message FROM SecurityEvents WHERE message LIKE ?", ('%' + keyword + '%',))
    data = cursor.fetchall()
    
    print(f"\n--- Search Results for '{keyword}' ---")
    for row in data:
        print(f"[{row[0]}] {row[1]}")
    conn.close()

if __name__ == "__main__":
    initialize_system()

    register_event_type("Login Success", "Informational")
    register_event_type("Login Failed", "Warning")
    register_event_type("Port Scan Detected", "Warning")
    register_event_type("Malware Alert", "Critical")

    register_source("Firewall_Main", "Server Room", "Firewall")
    register_source("App_Server_1", "Cloud AWS", "Server")
    register_source("Workstation_42", "HR Department", "Endpoint")

    log_security_event("App_Server_1", "Login Success", "Authorized access", "192.168.1.50", "admin")
    log_security_event("Firewall_Main", "Port Scan Detected", "Suspicious activity on port 22", "45.33.22.11")
    log_security_event("Workstation_42", "Malware Alert", "Ransomware detected by antivirus", "192.168.1.104", "hr_user")

    attacker_ip = "105.204.1.99"
    for i in range(8):
        log_security_event("App_Server_1", "Login Failed", f"Invalid password attempt #{i+1}", attacker_ip, "root")

    get_failed_logins_24h()
    analyze_brute_force()
    report_critical_events()
    search_messages("Ransomware")
