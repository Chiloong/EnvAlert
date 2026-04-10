import requests
import os
import json

LAT = 35.21
LON = 113.29

QWEATHER_API = "https://devapi.qweather.com/v7/weather/now"
WAQI_API = "https://api.waqi.info/feed/geo:{lat};{lon}/?token={token}"

QWEATHER_KEY = os.environ.get("QWEATHER_KEY")
WAQI_TOKEN = os.environ.get("WAQI_TOKEN")


# ========================
# 🌍 数据获取
# ========================
def fetch_all():
    print("🌍 开始获取数据...")

    url = f"{QWEATHER_API}?location={LON},{LAT}&key={QWEATHER_KEY}"

    try:
        weather = requests.get(url, timeout=10).json()
    except Exception as e:
        print("❌ QWeather失败:", e)
        return None

    if not weather or weather.get("code") != "200" or "now" not in weather:
        print("❌ QWeather异常")
        return None

    now = weather["now"]

    pressure = float(now.get("pressure", 0))
    humidity = float(now.get("humidity", 0))
    wind_speed = float(now.get("windSpeed", 0))
    wind_dir = now.get("windDir", "")
    wind_scale = now.get("windScale", "")

    # AQI
    aqi = 0
    try:
        waqi_url = WAQI_API.format(lat=LAT, lon=LON, token=WAQI_TOKEN)
        waqi = requests.get(waqi_url, timeout=10).json()
        if waqi.get("status") == "ok":
            aqi = waqi["data"]["aqi"]
    except:
        pass

    return {
        "pressure": pressure,
        "humidity": humidity,
        "wind_speed": wind_speed,
        "wind_dir": wind_dir,
        "wind_scale": wind_scale,
        "aqi": aqi
    }


# ========================
# 💾 状态
# ========================
STATE_FILE = "state.json"


def load_state():
    if not os.path.exists(STATE_FILE):
        return []
    try:
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    except:
        return []


def save_state(data):
    history = load_state()
    history.append(data)
    history = history[-72:]
    with open(STATE_FILE, "w") as f:
        json.dump(history, f)


# ========================
# 🧠 ①②③增强核心
# ========================
def calc_trend(history):
    n = len(history)

    # 🧠 ① 冷启动提示
    if n < 5:
        return f"📈趋势: 正在建立基线（{n}/5）"

    pressures = [x.get("pressure", 0) for x in history]
    aqis = [x.get("aqi", 0) for x in history]

    dp = pressures[-1] - pressures[0]
    daqi = aqis[-1] - aqis[0]

    # 🧠 ② 轻预测
    if abs(dp) < 1:
        p_trend = "气压稳定"
    elif dp > 0:
        p_trend = "气压上升"
    else:
        p_trend = "气压下降"

    if daqi > 5:
        a_trend = "AQI上升"
    elif daqi < -5:
        a_trend = "AQI下降"
    else:
        a_trend = "AQI稳定"

    # 🧠 ③ 人体影响模型（轻规则）
    impact = []

    if dp < -3:
        impact.append("可能疲劳")
    if daqi > 10:
        impact.append("空气质量压力")
    if float(history[-1].get("wind_speed", 0)) > 15:
        impact.append("风压刺激")

    impact_text = " / ".join(impact) if impact else "状态稳定"

    return (
        "📈12h趋势\n"
        f"{p_trend} ({dp:+.1f})\n"
        f"{a_trend} ({daqi:+.0f})\n"
        f"⚠️影响: {impact_text}"
    )


# ========================
# 📲 Bark
# ========================
def send_bark(msg):
    key = os.environ.get("BARK_KEY")
    if not key:
        print("❌ 没有BARK_KEY")
        return

    url = f"https://api.day.app/{key}/{msg}"

    try:
        requests.get(url, timeout=10)
        print("📲 已推送")
    except Exception as e:
        print("❌ Bark失败:", e)


# ========================
# 🚀 主流程
# ========================
def check_all():
    data = fetch_all()
    if not data:
        print("❌ 失败")
        return

    save_state(data)
    history = load_state()

    trend = calc_trend(history)

    msg = "\n".join([
        "🌍环境监测",
        f"气压:{data['pressure']}",
        f"湿度:{data['humidity']}%",
        f"风:{data['wind_dir']} {data['wind_scale']}级 ({data['wind_speed']})",
        f"AQI:{data['aqi']}",
        "",
        trend
    ])

    print("📨\n", msg)

    send_bark(msg)
