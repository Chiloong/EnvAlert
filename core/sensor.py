import requests
from config import LAT, LON, QWEATHER_KEY, WAQI_TOKEN

QWEATHER_API = "https://devapi.qweather.com/v7/weather/now"
WAQI_API = "https://api.waqi.info/feed/geo:{lat};{lon}/?token={token}"

def fetch_all():
    print("sensor start")

    # ── QWeather ──
    try:
        url = f"{QWEATHER_API}?location={LON},{LAT}&key={QWEATHER_KEY}"
        w = requests.get(url, timeout=10).json()
        now = w.get("now", {})
    except Exception as e:
        print("QWeather error:", e)
        return None

    # ── WAQI ──
    aqi = 0
    try:
        aqi_url = WAQI_API.format(lat=LAT, lon=LON, token=WAQI_TOKEN)
        a = requests.get(aqi_url, timeout=10).json()
        if a.get("status") == "ok":
            aqi_data = a.get("data", {})
            aqi = aqi_data.get("aqi", 0) if isinstance(aqi_data, dict) else 0
    except Exception as e:
        print("WAQI error:", e)

    return {
        "pressure":   float(now.get("pressure", 0)),
        "humidity":   float(now.get("humidity", 0)),
        "wind_dir":   now.get("windDir", ""),
        "wind_angle": float(now.get("wind360", 0)),
        "wind_scale": now.get("windScale", ""),
        "wind_speed": float(now.get("windSpeed", 0)),
        "aqi":        aqi
    }
