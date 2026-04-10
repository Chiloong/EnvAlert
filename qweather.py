import requests
from config import *

def get_all():
    params = {
        "location": f"{LON},{LAT}",
        "key": QWEATHER_API_KEY
    }

    w = requests.get(QWEATHER_NOW, params=params, timeout=10).json()["now"]
    a = requests.get(QWEATHER_AIR, params=params, timeout=10).json()["now"]

    return {
        "pressure": float(w["pressure"]),
        "humidity": float(w["humidity"]),
        "wind_speed": float(w["windSpeed"]),
        "wind_dir": float(w["wind360"]),
        "aqi": int(a["aqi"])
    }
