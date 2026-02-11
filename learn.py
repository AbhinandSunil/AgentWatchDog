import sqlite3, json, statistics, subprocess, datetime
conn = sqlite3.connect("history.db")
cursor = conn.execute("SELECT action, success FROM events WHERE ts > datetime('now','-1 day')")
data = cursor.fetchall()
restart_ok = [row[1] for row in data if row[0]=="restart"]
if restart_ok and statistics.mean(restart_ok) < 0.5:
    print("restart success < 50 %; scheduling reboot instead")
    subprocess.run(["shutdown", "/r", "/t", "300"])