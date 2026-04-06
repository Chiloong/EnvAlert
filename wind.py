import requests
import os

LAT = 35.21
LON = 113.29

API_KEY = os.environ["API_KEY"]
BARK_KEY = os.environ["BARK_KEY"]

STATE_FILE = "wind_state.txt"

WIND_SPEED_THRESHOLD = 2.5
GUST_THRESHOLD = 4.0
NE_MIN = 20
NE_MAX = 100

def send_bark(msg):
    try:
        url = f"https://api.day.app/{BARK_KEY}/{msg}"
        print("🚀 Bark URL:", url)
        r = requests.get(url, timeout=10)
        print("📡 Bark状态码:", r.status_code)
    except Exception as e:
        print("❌ Bark错误:", e)

def load_last_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return f.read().strip()
    return "OFF"

def save_state(state):
    with open(STATE_FILE, "w") as f:
        f.write(state)

def check_wind():
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={LAT}&lon={LON}&appid={API_KEY}&units=metric"
        data = requests.get(url, timeout=10).json()
        wind = data.get("wind", {})
        speed = wind.get("speed", 0)
        gust = wind.get("gust", 0)
        deg = wind.get("deg", -1)

        speed_ok = speed >= WIND_SPEED_THRESHOLD or gust >= GUST_THRESHOLD
        direction_ok = NE_MIN <= deg <= NE_MAX

        current_state = "ON" if (speed_ok and direction_ok) else "OFF"
        last_state = load_last_state()

        if last_state == "OFF" and current_state == "ON":
            send_bark(f"🏭 发电厂↙️东北风触发\n风速:{speed}ms\n阵风:{gust}ms\n风向:{deg}°")

        save_state(current_state)
        print(f"🌬 风速:{speed} | 风向:{deg}")
        return speed, deg

    except Exception as e:
        print("❌ Wind Error:", e)
        return 0, -1
