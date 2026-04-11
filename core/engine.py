from config import *


def detect(data, prev):
    events = []

    angle = data.get("wind_angle", 0)

    # 🌬️东北风
    if 20 <= angle <= 100:
        events.append("wind_ne")

    # 🌨️气压低
    if data["pressure"] < PRESSURE_LOW:
        events.append("pressure_low")

    # 😷AQI高
    if data["aqi"] > AQI_HIGH:
        events.append("aqi_high")

    # 🌫️湿度高
    if data["humidity"] > HUMIDITY_HIGH:
        events.append("humidity_high")

    # 📉ΔP
    if prev:
        dp = data["pressure"] - prev["pressure"]
        dp_abs = abs(dp)

        if dp_abs < DP_WEAK:
            dp_level = "🟢弱波动"
        elif dp_abs < DP_STRONG:
            dp_level = "🟡中波动"
        else:
            dp_level = "🔴强波动"
    else:
        dp = 0
        dp_level = "🟢弱波动"

    # 🧠风险评分（简单版）
    risk = 0

    if "pressure_low" in events:
        risk += 30
    if "aqi_high" in events:
        risk += 30
    if "humidity_high" in events:
        risk += 20
    if "wind_ne" in events:
        risk += 20

    if "🔴" in dp_level:
        risk += 20
    elif "🟡" in dp_level:
        risk += 10

    risk = min(risk, 100)

    return events, dp_level, risk
