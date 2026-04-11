import requests
from config import BARK_KEY
from urllib.parse import quote


def send(msg):
    print("bark send")

    # 🔥关键：URL编码
    safe_msg = quote(msg)

    url = f"https://api.day.app/{BARK_KEY}/{safe_msg}"

    try:
        r = requests.get(url, timeout=10)
        print(r.status_code)
    except:
        print("bark error")
