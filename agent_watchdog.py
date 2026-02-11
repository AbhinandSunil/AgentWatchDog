import psutil, time, json, sqlite3, subprocess, openai, os, datetime
import deep_diag  # our diagnostics module

CONFIG = {
    "exes": ["MonitorFile.exe"],          # file to monitor
    "poll_secs": 5,
    "backoff": [5, 10, 30, 60],
    "openai_key": os.getenv("OPENAI_API_KEY"),
    "brain_prompt": open("brain_enhanced.txt").read()
}

conn = sqlite3.connect("history.db", isolation_level=None)
openai_client = openai.OpenAI(base_url="http://localhost:xxxxx/v1", api_key="ollama")

# ---------- DB init (run once) ----------
conn.execute("""CREATE TABLE IF NOT EXISTS events(
    ts TEXT, exe TEXT, exit_code INTEGER, action TEXT, success INTEGER)""")
conn.execute("""CREATE TABLE IF NOT EXISTS reports(
    ts TEXT, exe TEXT, report_json TEXT)""")

def log(exe, exit_code, action, success):
    conn.execute("INSERT INTO events VALUES(?,?,?,?,?)",
                (datetime.datetime.utcnow().isoformat(), exe, exit_code, action, success))

def llm_decide(blob):
    resp = openai_client.chat.completions.create(
        model="llama3.2:3b",
        messages=[{"role": "system", "content": CONFIG["brain_prompt"]},
                  {"role": "user", "content": json.dumps(blob)}],
        temperature=0)
    return json.loads(resp.choices[0].message.content)

def restart_exe(exe, sleep):
    print(f"[ACT] restarting {exe} in {sleep}s")
    time.sleep(sleep)
    subprocess.Popen(["start", "", exe], shell=True)

def reboot():
    print("[ACT] rebooting system")
    subprocess.run(["shutdown", "/r", "/t", "30"])

def check():
    running = {p.name(): p for p in psutil.process_iter(['pid', 'name'])}
    all_ok = True
    for exe in CONFIG["exes"]:
        log_path = deep_diag.find_log_file(exe)
        proc = running.get(exe)
        exit_code = None

        if proc:  # ---------- stall check ----------
            if deep_diag.is_stalled(proc, log_path):
                all_ok = False
            else:
                continue  # healthy
        else:  # ---------- crashed ----------
            all_ok = False
            row = conn.execute("SELECT exit_code FROM events WHERE exe=? ORDER BY ts DESC LIMIT 1", (exe,)).fetchone()
            exit_code = row[0] if row else 0

        # ---------- decide ----------
        log_snippet = deep_diag.tail_log(log_path)
        decision = llm_decide({"exe": exe, "exit_code": exit_code, "logs": log_snippet or ""})
        report = decision.get("report", {})
        conn.execute("INSERT INTO reports VALUES(?,?,?)",
                    (datetime.datetime.utcnow().isoformat(), exe, json.dumps(report)))

        # ---------- act ----------
        if decision["action"] == "restart":
            restart_exe(exe, decision["params"].get("sleep", CONFIG["backoff"][0]))
            log(exe, exit_code, "restart", 1)
        elif decision["action"] == "reboot":
            reboot()
            log(exe, exit_code, "reboot", 1)
        else:
            log(exe, exit_code, "nothing", 1)

    if all_ok:
        print({"action": "nothing", "reason": "all processes running", "params": {}})

if __name__ == "__main__":
    while True:
        try:
            check()
        except Exception as e:
            print("loop error", e)
        time.sleep(CONFIG["poll_secs"])