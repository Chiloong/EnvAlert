import requests
import time

API_KEY = "你的OpenWeatherKey"
CITY = "Tokyo"

BARK_KEY = "你的BarkKey"

def get_pressure():
    url = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}"
    data = requests.get(url).json()
    return data["main"]["pressure"]

def send_bark(msg):
    url = f"https://api.day.app/{BARK_KEY}/{msg}"
    requests.get(url)

def main():
    # 获取当前气压
    p1 = get_pressure()
    time.sleep(600)  # 等10分钟
    p2 = get_pressure()

    delta_p = p2 - p1
    rate = delta_p / (10/60)  # 转成 hPa/h

    print(f"变化速率: {rate:.2f} hPa/h")

    # 预警逻辑
    if abs(rate) > 1.5:
        send_bark(f"⚠️气压异常 {rate:.2f} hPa/h")

if __name__ == "__main__":
    main()
