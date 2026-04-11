import requests
from config import BARK_KEY

def send(msg):
    print("bark send:", msg[:30])
    try:
        lines = msg.split("\n")
        title = lines[0]
        body  = "\n".join(lines[1:])
        r = requests.post(
            "https://api.day.app/push",
            json={"device_key": BARK_KEY, "title": title, "body": body},
            timeout=10
        )
        print(r.status_code, r.text)
        return r.status_code == 200
    except Exception as e:
        print("bark error:", e)
        return False  # 修复：返回成功/失败，供 main.py 判断
