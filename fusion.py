import requests
import os
import time

LAT = 35.21
LON = 113.29

QWEATHER_API = "https://devapi.qweather.com/v7/weather/now"
WAQI_API = "https://api.waqi.info/feed/geo:{lat};{lon}/?token={token}"

QWEATHER_KEY = os.environ.get("QWEATHER_KEY")
WAQI_TOKEN = os.environ.get("WAQI_TOKEN")


def fetch_all():
    print("🌍 开始获取数据...")

    # ========================
    # 🌤 QWeather
    # ========================
    weather_url = f"{QWEATHER_API}?location={LON},{LAT}&key={QWEATHER_KEY}"
    print("🔑 KEY:", QWEATHER_KEY)
    print("🌐 URL:", weather_url)

    try:
        weather = requests.get(weather_url, timeout=10).json()
    except Exception as e:
        print("❌ QWeather请求失败:", e)
        return None

    print("📦 QWeather返回:", weather)

    # ❗核心防炸
    if not weather or weather.get("code") != "200" or "now" not in weather:
        print("❌ QWeather数据异常")
        return None

    now = weather["now"]

    pressure = float(now.get("pressure", 0))
    humidity = float(now.get("humidity", 0))
    wind_speed = float(now.get("windSpeed", 0))
    wind_dir = float(now.get("wind360", 0))

    # ========================
    # 🌫 AQI（WAQI）
    # ========================
    aqi = 0
    try:
        waqi_url = WAQI_API.format(lat=LAT, lon=LON, token=WAQI_TOKEN)
        waqi = requests.get(waqi_url, timeout=10).json()
        print("📦 WAQI返回:", waqi)

        if waqi.get("status") == "ok":
            aqi = waqi["data"]["aqi"]
        else:
            print("⚠️ WAQI异常")
    except Exception as e:
        print("⚠️ WAQI请求失败:", e)

    return {
        "pressure": pressure,
        "humidity": humidity,
        "wind_speed": wind_speed,
        "wind_dir": wind_dir,
        "aqi": aqi
    }


# ========================
# 📈 趋势计算（12小时）
# ========================
STATE_FILE = "state.json"


def load_state():
    if not os.path.exists(STATE_FILE):
        return []
    try:
        import json
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    except:
        return []


def save_state(data):
    import json
    history = load_state()
    history.append(data)

    # 只保留最近12小时（假设10分钟一次≈72条）
    history = history[-72:]

    with open(STATE_FILE, "w") as f:
        json.dump(history, f)


def calc_trend(history):
    if not history:
        return ""

    pressures = [x["pressure"] for x in history]
    aqis = [x["aqi"] for x in history]

    return f"📈12h趋势\n气压↓{min(pressures)}\nAQI↑{max(aqis)}"


# ========================
# 🔔 Bark推送
# ========================
def send_bark(msg):
    BARK_KEY = os.environ.get("BARK_KEY")
    if not BARK_KEY:
        print("❌ 没有BARK_KEY")
        return

    url = f"https://api.day.app/{BARK_KEY}/{msg}"
    try:
        requests.get(url)
        print("📲 已推送")
    except:
        print("❌ 推送失败")


# ========================
# 🚀 主逻辑
# ========================
def check_all():
    data = fetch_all()

    if not data:
        print("❌ 数据获取失败，终止")
        return

    save_state(data)
    history = load_state()

    trend = calc_trend(history)

    msg = (
        f"🌍环境监测\n"
        f"气压:{data['pressure']}\n"
        f"湿度:{data['humidity']}%\n"
        f"风:{data['wind_speed']}m/s\n"
        f"AQI:{data['aqi']}\n\n"
        f"{trend}"
    )

    print("📨 推送内容:\n", msg)

    send_bark(msg)
