import json, os, time

STATE_FILE     = "storage/event_state.json"
HEARTBEAT_FILE = "storage/heartbeat.json"

def load(path, default):
    if not os.path.exists(path):
        return default
    try:
        with open(path, "r") as f:
            return json.load(f)
    except:
        return default

def safe_save(path, data):
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            json.dump(data, f)
    except Exception as e:
        print("[State] save error:", e)

def can_trigger(key, cooldown=1800):
    """只判断是否可以触发，不写入状态"""
    state = load(STATE_FILE, {})
    return time.time() - state.get(key, 0) >= cooldown

def mark_triggered(key):
    """发送成功后再标记，避免发送失败导致冷却白白消耗"""
    state = load(STATE_FILE, {})
    state[key] = time.time()
    safe_save(STATE_FILE, state)

def clear_event(key):
    """事件恢复正常后清除冷却状态，下次触发不受旧记录影响"""
    state = load(STATE_FILE, {})
    if key in state:
        del state[key]
        safe_save(STATE_FILE, state)

def heartbeat_due(interval):
    hb = load(HEARTBEAT_FILE, {"t": 0})
    now = time.time()
    if now - hb["t"] > interval:
        hb["t"] = now
        safe_save(HEARTBEAT_FILE, hb)
        return True
    return False
