```python
import requests
import time
import os
from config import BARK_KEY, TREND_PRESSURE_ACCEL_THRESHOLD, WIND_SPEED_THRESHOLD

HEARTBEAT_FILE = "heartbeat.txt"
EVENT_FILE = "last_event.txt"
STATE_FILE = "fusion_state.txt"

HEARTBEAT_INTERVAL = 43200  # 12小时

def send_bark(msg):
    try:
        requests.get(f"https://api.day.app/{BARK_KEY}/{msg}", timeout=10)
    except:
        pass

def read_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return f.read().strip()
    return "OFF"

def save_state(s):
    with open(STATE_FILE, "w") as f:
        f.write(s)

def record_event():
    with open(EVENT_FILE, "w") as f:
        f.write(str(time.time()))

def read_last_event():
    try:
        with open(EVENT_FILE, "r") as f:
            return float(f.read().strip())
    except:
        return 0

def read_last_heartbeat():
    try:
        with open(HEARTBEAT_FILE, "r") as f:
            return float(f.read().strip())
    except:
        return 0

def save_heartbeat(t):
    with open(HEARTBEAT_FILE, "w") as f:
        f.write(str(t))

def smart_heartbeat():
    now = time.time()
    last_event = read_last_event()
    last_heartbeat = read_last_heartbeat()

    if (now - last_event > HEARTBEAT_INTERVAL) and (now - last_heartbeat > HEARTBEAT_INTERVAL):
        send_bark("🟢EnvAlert正常运行（无异常）")
        save_heartbeat(now)
        print("🟢 心跳发送")

def check_fusion(wind_data, pressure_data):
    print("🧠 趋势联动运行")

    wind_speed, wind_deg = wind_data
    rate, accel = pressure_data

    last_state = read_state()
    current_state = "OFF"

    # ⚡ 判断是否进入“异常状态”
    if accel < -TREND_PRESSURE_ACCEL_THRESHOLD or wind_speed > WIND_SPEED_THRESHOLD:
        current_state = "ON"

    # ✅ 只在 OFF → ON 时触发（核心修复）
    if last_state == "OFF" and current_state == "ON":
        send_bark("🚨环境趋势异常触发")
        record_event()

    save_state(current_state)

    # 🟢 智能心跳
    smart_heartbeat()

    print("✅ 联动完成")
```
