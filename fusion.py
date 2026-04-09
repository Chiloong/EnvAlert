import os
import requests
from config import *
from wind import get_wind
from pressure import get_pressure_signals
from aqi import get_aqi

# ======================
# 🔔 发送通知
# ======================
def send(msg):
    try:
        requests.get(f"{BARK_URL}/{BARK_KEY}/{msg}", timeout=10)
    except:
        pass

# ======================
# 📂 读取状态（兼容旧版本）
# ======================
def read_state():
    if not os.path.exists(STATE_FILE):
        return 0

    try:
        content = open(STATE_FILE).read().strip()

        # ✅ 兼容旧版本 ON / OFF
        if content == "ON":
            return 1
        if content == "OFF":
            return 0

        return int(content)

    except:
        return 0

# ======================
# 💾 保存状态
# ======================
def save_state(v):
    try:
        with open(STATE_FILE, "w") as f:
            f.write(str(v))
    except:
        pass

# ======================
# 🧠 核心联动逻辑（稳定版）
# ======================
def check_all():

    # 获取各模块状态
    wind_t = get_wind()
    low_t, rate_t = get_pressure_signals()
    aqi_t = get_aqi()

    # 当前触发数量
    count = sum([wind_t, low_t, rate_t, aqi_t])

    # 上一次状态
    last = read_state()

    msg = None

    # ======================
    # 🚨 只在“升级”时触发
    # ======================
    if count > last:

        # 单项触发
        if count == 1:
            if wind_t:
                msg = "🚨EnvAlert🚨\n🏭发电厂↙️东北风💨触发\n⛔️关闭新风🟣颗粒过滤开大⬆️"
            elif low_t:
                msg = "🚨EnvAlert🚨\n✴️气压🌨️过低🥱"
            elif rate_t:
                msg = "🚨EnvAlert🚨\n✴️气压〽️骤变😣"
            elif aqi_t:
                msg = "🚨EnvAlert🚨\n🟥高污染😷"

        # 联动升级
        elif count == 2:
            msg = "🟡气象预警🚨"
        elif count == 3:
            msg = "🟠气象预警🚨"
        elif count == 4:
            msg = "🔴气象预警🚨"

    # ======================
    # 🔔 发送
    # ======================
    if msg:
        send(msg)

    # ======================
    # 💾 保存状态
    # ======================
    save_state(count)

    print(f"当前:{count} 上次:{last}")
