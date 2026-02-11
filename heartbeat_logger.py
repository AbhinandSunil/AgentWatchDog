import time, json, datetime, os, signal
LOG = open(r"C:\AgentWatchdog\airport.log","a", buffering=1)
def sigterm(*_): LOG.close(); os._exit(0)
signal.signal(signal.SIGTERM, sigterm)
while True:
    LOG.write(json.dumps({"ts":datetime.datetime.utcnow().isoformat(),"type":"heartbeat"})+"\n")
    time.sleep(30)