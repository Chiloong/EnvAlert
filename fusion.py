import requests
from config import BARK_KEY, TREND_PRESSURE_ACCEL_THRESHOLD, WIND_SPEED_THRESHOLD

def send_bark(msg):
    try:
        requests.get(f"https://api.day.app/{BARK_KEY}/{msg}", timeout=10)
    except:
        pass

def check_fusion(wind_data, pressure_data):
    print("🧠 趋势联动运行")

    wind_speed, wind_deg = wind_data
    rate, accel = pressure_data

    # ⚡ 气压加速下降（核心预警）
    if accel < -TREND_PRESSURE_ACCEL_THRESHOLD:
        send_bark(f"⚡气压加速下降 {accel:.2f}")

    # 🌬 风增强
    if wind_speed > WIND_SPEED_THRESHOLD:
        send_bark(f"🌬风增强 {wind_speed:.1f}")

    # 🚨 联动预警（重点）
    if accel < -0.3 and wind_speed > WIND_SPEED_THRESHOLD:
        send_bark("🚨环境恶化趋势（气压↓+风↑）")

    print("✅ 联动完成")
