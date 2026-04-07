import requests
import time
from config import BARK_KEY, TREND_PRESSURE_ACCEL_THRESHOLD, WIND_SPEED_THRESHOLD

HEARTBEAT_FILE = "heartbeat.txt"
EVENT_FILE = "last_event.txt"

# ⏱ 心跳间隔（无事件多久才发）
HEARTBEAT_INTERVAL = 43200   # 12小时

def send_bark(msg):
    try:
        requests.get(f"https://api.day.app/{BARK_KEY}/{msg}", timeout=10)
    except:
        pass

def record_event():
    try:
        with open(EVENT_FILE, "w") as f:
            f.write(str(time.time()))
    except:
        pass

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
    try:
        with open(HEARTBEAT_FILE, "w") as f:
            f.write(str(t))
    except:
        pass

def smart_heartbeat():
    try:
        now = time.time()
        last_event = read_last_event()
        last_heartbeat = read_last_heartbeat()

        # 🧠 核心逻辑：
        # 👉 长时间没有任何“异常事件”才发心跳
        if (now - last_event > HEARTBEAT_INTERVAL) and (now - last_heartbeat > HEARTBEAT_INTERVAL):
            send_bark("🟢EnvAlert正常运行（无异常）")
            save_heartbeat(now)
            print("🟢 智能心跳发送")

    except Exception as e:
        print("❌ 心跳错误:", e)

def check_fusion(wind_data, pressure_data):
    print("🧠 趋势联动运行")

    wind_speed, wind_deg = wind_data
    rate, accel = pressure_data

    triggered = False

    # ⚡ 气压加速下降（核心预警）
    if accel < -TREND_PRESSURE_ACCEL_THRESHOLD:
        send_bark(f"⚡气压加速下降 {accel:.2f}")
        triggered = True

    # 🌬 风增强
    if wind_speed > WIND_SPEED_THRESHOLD:
        send_bark(f"🌬风增强 {wind_speed:.1f}")
        triggered = True

    # 🚨 联动预警（重点）
    if accel < -0.3 and wind_speed > WIND_SPEED_THRESHOLD:
        send_bark("🚨环境恶化趋势（气压↓+风↑）")
        triggered = True

    # 🧠 如果有事件 → 记录时间（抑制心跳）
    if triggered:
        record_event()

    # 🟢 智能心跳（仅在“长时间无事件”才触发）
    smart_heartbeat()

    print("✅ 联动完成")
