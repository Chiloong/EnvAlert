import requests
from config import *
import time

def get_aqi_signals():
    try:
        url = WAQI_URL.format(lat=LAT, lon=LON, token=WAQI_TOKEN)
        res = requests.get(url, timeout=10).json()
        if res.get("status") != "ok":
            return False, False, 0
        aqi = res["data"]["aqi"]
        last_aqi_file = "aqi_last.txt"
        try:
            last_aqi = int(open(last_aqi_file).read().strip())
        except:
            last_aqi = aqi
        dt = 1  # 简化：假设每次运行间隔约1小时
        aqi_rate = (aqi - last_aqi)/dt
        rise_flag = aqi_rate > 10  # AQI快速上升阈值，可调
        high_flag = aqi >= AQI_THRESHOLD
        open(last_aqi_file, "w").write(str(aqi))
        return high_flag, rise_flag, aqi
    except:
        return False, False, 0
