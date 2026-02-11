import os
import psutil
import time
import datetime
import subprocess
import re
import json
import logging
from pygtail import Pygtail

LOG_FOLDERS = [
    os.path.expandvars(r"%PROGRAMDATA%\MyCompany\logs"),
    os.path.expandvars(r"%LOCALAPPDATA%\MyCompany\logs"),
    os.path.expanduser(r"~\Documents\MyCompany\logs")
]

def find_log_file(exe_name: str):
    """Return newest *.log file that contains exe_name stem."""
    stem = os.path.splitext(exe_name)[0].lower()
    for folder in LOG_FOLDERS:
        if not os.path.isdir(folder):
            continue
        for fn in sorted(os.listdir(folder),
                         key=lambda x: os.path.getmtime(os.path.join(folder, x)),
                         reverse=True):
            if stem in fn.lower() and fn.endswith('.log'):
                return os.path.join(folder, fn)
    return None

def tail_log(log_path, last_bytes=4096):
    """Return last ≤ last_bytes of log (handles rotation)."""
    if not log_path or not os.path.exists(log_path):
        return None
    try:
        # Pygtail returns the unread portion; we just want the tail
        tail = Pygtail(log_path, read_from_end=True).read()
        return tail[-last_bytes:] if len(tail) > last_bytes else tail
    except Exception as e:
        logging.exception("tail_log")
        return None

def is_stalled(proc, log_path, idle_seconds=60):
    """True if CPU% < 1 and log file unchanged for idle_seconds."""
    try:
        cpu = proc.cpu_percent(interval=1.0)
        if cpu > 1.0:
            return False
        if not log_path:
            return True  # no log → treat as stalled
        mtime = os.path.getmtime(log_path)
        return (time.time() - mtime) > idle_seconds
    except (psutil.NoSuchProcess, FileNotFoundError):
        return False

def build_report(exe, exit_code, log_snippet):
    """Call same local LLM you already use to fill the ‘report’ section."""
    from openai import OpenAI
    client = OpenAI(base_url="http://localhost:xxxxx/v1", api_key="ollama")
    prompt = open("brain_enhanced.txt", encoding="utf-8").read()
    blob = {
        "exe": exe,
        "exit_code": exit_code,
        "logs": log_snippet or ""
    }
    resp = client.chat.completions.create(
        model="llama3.2:3b",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": json.dumps(blob)}
        ],
        temperature=0
    )
    return json.loads(resp.choices[0].message.content)