import requests
import os
import time

LAT = 35.21
LON = 113.29

API_KEY = os.environ["API_KEY"]
BARK_KEY = os.environ["BARK_KEY"]

STATE_FILE = "pressure_state.txt"
TREND_COUNT = 3        # 连续下降/上升点数
RATE_THRESHOLD = 1.5   # hPa/h，触发阈值


def send_bark(msg):
    try:
        url = f"https://api.day.app/{BARK_KEY}/{msg}"
        print("🚀 Bark URL:", url)
        r = requests.get(url, timeout=10)
        print("📡 Bark状态码:", r.status_code)
    except Exception as e:
        print("❌ Bark错误:", e)


def get_pressure():
    url = (
        f"https://api.openweathermap.org/data/2.5/weather?"
        f"lat={LAT}&lon={LON}&appid={API_KEY}&units=metric"
    )
    print("🌍 请求天气数据...")
    data = requests.get(url, timeout=10).json()
    return data["main"]["pressure"]


def read_history():
    """读取历史数据，返回列表 [(p, t), ...]"""
    try:
        with open(STATE_FILE, "r") as f:
            lines = f.readlines()
        history = []
        for line in lines[-TREND_COUNT:]:
            p, t = line.strip().split(",")
            history.append((float(p), float(t)))
        print("📂 历史数据:", history)
        return history
    except Exception as e:
        print("📂 无历史数据:", e)
        return []


def save_current(p, t):
    with open(STATE_FILE, "a") as f:
        f.write(f"{p},{t}\n")
    print("💾 已保存当前数据")


def check_trend(history, current_p, current_t):
    """判断气压趋势"""
    trend_triggered = False
    history.append((current_p, current_t))
    if len(history) >= TREND_COUNT:
        rates = []
        for i in range(1, len(history)):
            delta_p = history[i][0] - history[i - 1][0]
            delta_t = (history[i][1] - history[i - 1][1]) / 3600
            if delta_t > 0:
                rate = delta_p / delta_t
                rates.append(rate)
        print("📈 各段速率:", rates)
        # 判断是否连续下降或上升
        if all(r <= -RATE_THRESHOLD for r in rates):
            trend_triggered = True
            direction = "📉下降"
            rate_avg = sum(rates)/len(rates)
        elif all(r >= RATE_THRESHOLD for r in rates):
            trend_triggered = True
            direction = "📈上升"
            rate_avg = sum(rates)/len(rates)
        else:
            direction = "STABLE"
            rate_avg = sum(rates)/len(rates)
        return trend_triggered, direction, rate_avg
    else:
        return False, "STABLE", 0.0


def check_pressure_and_wind(wind_speed=None, wind_dir=None):
    print("🔥 trend pressure模块已执行")
    try:
        current_p = get_pressure()
        current_t = time.time()
        print(f"🌡 当前气压: {current_p} hPa")

        history = read_history()
        trend_triggered, direction, rate_avg = check_trend(history, current_p, current_t)
        print(f"📊 速率平均: {rate_avg:.2f} hPa/h | 趋势: {direction}")

        # ⚠️ 联动逻辑
        risk = False
        risk_msg = ""
        if trend_triggered:
            # 风条件可选
            if wind_speed is not None and wind_dir is not None:
                if 60 <= wind_dir <= 135:  # 东北风范围
                    risk = True
                    risk_msg = f"🌬 东北风 {wind_speed:.2f} m/s + 气压趋势 {direction} {rate_avg:.2f} hPa/h"
            else:
                # 没给风参数时只依赖气压趋势
                risk = True
                risk_msg = f"🌡 气压趋势 {direction} {rate_avg:.2f} hPa/h"

        # 强制测试推送链路
        send_bark("✅ 气压趋势模块运行成功（测试）")

        if risk:
            send_bark(f"🚨 高风险环境触发: {risk_msg}")

        save_current(current_p, current_t)

    except Exception as e:
        print("❌ Trend Pressure Error:", e)
