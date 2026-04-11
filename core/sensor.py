import requests
from config import *

QWEATHER_API = "https://devapi.qweather.com/v7/weather/now"
WAQI_API = "https://api.waqi.info/feed/geo:{lat};{lon}/?token={token}"


def fetch_all():
    print("sensor start")

    try:
        url = f"{QWEATHER_API}?location={LON},{LAT}&key={QWEATHER_KEY}"
        w = requests.get(url, timeout=10).json()
        now = w.get("now", {})
    except:
        return None

    try:
        aqi_url = WAQI_API.format(lat=LAT, lon=LON, token=WAQI_TOKEN)
        a = requests.get(aqi_url, timeout=10).json()
    except:
        a = {}

    return {
        "pressure": float(now.get("pressure", 0)),
        "humidity": float(now.get("humidity", 0)),
        "wind_dir": now.get("windDir", ""),
        "wind_angle": float(now.get("wind360", 0)),
        "wind_scale": now.get("windScale", ""),
        "wind_speed": float(now.get("windSpeed", 0)),
        "aqi": a.get("data", {}).get("aqi", 0) if isinstance(a, dict) else 0
    }
