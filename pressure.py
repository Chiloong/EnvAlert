import requests
import time
from config import OPENWEATHER_URL, BARK_URL, LAT, LON, API_KEY, BARK_KEY
from config import PRESSURE_STATE_FILE, PRESSURE_RATE_THRESHOLD

def send_bark(msg):
    try:
        url = f"{BARK_URL}/{BARK_KEY}/{msg}"
        print("🚀 Bark URL:", url)
        r = requests.get(url, timeout=10)
        print("📡 Bark状态码:", r.status_code)
    except Exception as e:
        print("❌ Bark错误:", e)

def get_pressure():
    print("🌍 请求天气数据...")
    data = requests.get(f"{OPENWEATHER_URL}?lat={LAT}&lon={LON}&appid={API_KEY}&units=metric", timeout=10).json()
    return data["main"]["pressure"]

def read_last():
    try:
        with open(PRESSURE_STATE_FILE, "r") as f:
            p, t = f.read().split(",")
            print("📂 读取历史:", p, t)
            return float(p), float(t)
    except Exception as e:
        print("📂 无历史数据:", e)
        return None

def save_current(p, t):
    with open(PRESSURE_STATE_FILE, "w") as f:
        f.write(f"{p},{t}")
    print("💾 已保存当前数据")

def check_pressure():
    print("🔥 pressure模块已执行")
    try:
        current_p = get_pressure()
        current_t = time.time()
        print(f"🌡 当前气压: {current_p} hPa")
        last = read_last()
        send_bark("✅气压模块运行成功（测试）")
        if last:
            last_p, last_t = last
            delta_p = current_p - last_p
            delta_t = (current_t - last_t) / 3600
            if delta_t > 0:
                rate = delta_p / delta_t
                print(f"📈 速率: {rate:.2f} hPa/h")
                if abs(rate) > PRESSURE_RATE_THRESHOLD:
                    direction = "📉下降" if rate < 0 else "📈上升"
                    send_bark(f"🌡气压异常 {direction} {rate:.2f} hPa/h")
        else:
            print("⚠️ 第一次运行，仅记录数据")
        save_current(current_p, current_t)
    except Exception as e:
        print("❌ Pressure Error:", e)
        return 0
