import json, os, time

STATE_FILE = "storage/event_state.json"
HEARTBEAT_FILE = "storage/heartbeat.json"

def load(path, default):
    if not os.path.exists(path):
        return default
    try:
        return json.load(open(path))
    except:
        return default

def save(path, data):
    json.dump(data, open(path, "w"))

def can_trigger(event, cooldown=1800):
    state = load(STATE_FILE, {})
    now = time.time()

    last = state.get(event, 0)
    if now - last < cooldown:
        return False

    state[event] = now
    save(STATE_FILE, state)
    return True

def heartbeat_due(interval):
    hb = load(HEARTBEAT_FILE, {"t": 0})
    now = time.time()

    if now - hb["t"] > interval:
        hb["t"] = now
        save(HEARTBEAT_FILE, hb)
        return True

    return False
