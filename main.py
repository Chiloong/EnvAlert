print("=== RUNNING ===")

from core.sensor    import fetch_all
from core.engine    import detect
from core.state     import can_trigger, mark_triggered, clear_event, heartbeat_due
from core.formatter import format_event, format_combo, format_heartbeat
from core.notifier  import send
from config         import HEARTBEAT_INTERVAL, EVENT_COOLDOWN

import json, os, tempfile

def log(msg):
    print(f"[EnvAlert] {msg}")

def load_prev():
    path = "storage/state.json"
    if not os.path.exists(path):
        return None
    try:
        with open(path, "r") as f:
            return json.load(f)
    except:
        return None

def save_state(data):
    os.makedirs("storage", exist_ok=True)
    with tempfile.NamedTemporaryFile("w", dir="storage", delete=False, suffix=".tmp") as f:
        json.dump(data, f)
        tmp = f.name
    os.replace(tmp, "storage/state.json")

def main():
    log("🚀 start")

    data = fetch_all()
    log(f"data={data}")
    if not data:
        log("ERROR: empty data")
        return

    prev = load_prev()
    events, dp_level, risk = detect(data, prev)
    log(f"events={events} dp_level={dp_level} risk={risk}")

    save_state(data)

    # =========================
    # 🌙 心跳
    # =========================
    if heartbeat_due(HEARTBEAT_INTERVAL):
        msg = format_heartbeat(data, dp_level, risk)
        log("heartbeat")
        send(msg)

    # =========================
    # 🔥 单事件独立推送
    # =========================
    for e in events:
        key = "single:" + e
        if can_trigger(key, EVENT_COOLDOWN):
            msg = format_event(e, data, dp_level, risk)
            log(f"single_event={e}")
            if send(msg):
                mark_triggered(key)

    # 事件恢复后清除冷却状态
    all_keys = ["wind_ne", "pressure_low", "aqi_high", "humidity_high", "pressure_change"]
    for e in all_keys:
        if e not in events:
            clear_event("single:" + e)

    # =========================
    # 🔥 组合事件推送
    # =========================
    if len(events) >= 2:
        combo_key = "combo:" + ",".join(sorted(events))
        if can_trigger(combo_key, EVENT_COOLDOWN):
            msg = format_combo(events, data, dp_level, risk)
            log(f"combo_event={events}")
            if send(msg):
                mark_triggered(combo_key)

if __name__ == "__main__":
    main()
