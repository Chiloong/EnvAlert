import requests
import os
from config import LAT, LON, API_KEY, BARK_KEY, WIND_SPEED_THRESHOLD, WIND_GUST_THRESHOLD, WIND_NE_MIN, WIND_NE_MAX, WIND_STATE_FILE

def send_bark(msg):
    try:
        url = f"{BARK_URL}/{BARK_KEY}/{msg}"
        print("🚀 Bark URL:", url)
        r = requests.get(url, timeout=10)
        print("📡 Bark状态码:", r.status_code)
    except:
        pass

def load_last_state():
    if os.path.exists(WIND_STATE_FILE):
        with open(WIND_STATE_FILE, "r") as f:
            return f.read().strip()
    return "OFF"

def save_state(state):
    with open(WIND_STATE_FILE, "w") as f:
        f.write(state)

def check_wind():
    try:
        url = f"{OPENWEATHER_URL}?lat={LAT}&lon={LON}&appid={API_KEY}&units=metric"
        data = requests.get(url, timeout=10).json()
        wind = data.get("wind", {})
        wind_speed = wind.get("speed", 0)
        wind_deg = wind.get("deg", -1)
        gust = wind.get("gust", 0)
        speed_ok = wind_speed >= WIND_SPEED_THRESHOLD or gust >= WIND_GUST_THRESHOLD
        direction_ok = WIND_NE_MIN <= wind_deg <= WIND_NE_MAX
        current_state = "ON" if (speed_ok and direction_ok) else "OFF"
        last_state = load_last_state()
        if last_state=="OFF" and current_state=="ON":
            send_bark(f"🏭发电厂↙️东北风触发\n风速:{wind_speed}ms\n阵风:{gust}ms\n风向:{wind_deg}°")
        save_state(current_state)
    except Exception as e:
        print("❌ Wind Error:", e)

# fusion.py
from wind import check_wind
from pressure import check_pressure
from config import PRESSURE_RATE_THRESHOLD, WIND_SPEED_THRESHOLD

def check_fusion():
    print("🧠 联动模块运行")
    # 先执行单模块
    check_wind()
    check_pressure()
    # ⚡ 联动逻辑示例
    # 可加入阈值判断，组合风速与气压下降速率 → 环境恶化预警
    print("🌬 风速/风向与🌡 气压联动完成")
