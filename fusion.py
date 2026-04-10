import time, json, requests
from config import *
from qweather import get_all

# ======================
# 工具
# ======================
def send(msg):
    try:
        requests.get(f"{BARK_URL}/{BARK_KEY}/{msg}", timeout=10)
    except:
        pass

def read_json(f, d):
    try:
        return json.load(open(f))
    except:
        return d

def save_json(f, d):
    json.dump(d, open(f, "w"))

# ======================
# ⏱ 动态频率
# ======================
def should_run(risk):
    now = time.time()
    last = read_json(RUN_STATE_FILE, {"t":0})["t"]

    if risk:
        interval = 300
    else:
        interval = 900

    if now - last < interval:
        return False

    save_json(RUN_STATE_FILE, {"t": now})
    return True

# ======================
# 趋势
# ======================
def calc_trend(file, val, threshold):
    now = time.time()
    last = read_json(file, {"v": val, "t": now})

    dt = (now - last["t"]) / 3600
    flag = False

    if dt > 0:
        rate = (val - last["v"]) / dt
        if threshold < 0:
            flag = rate <= threshold
        else:
            flag = rate >= threshold

    save_json(file, {"v": val, "t": now})
    return flag

# ======================
# 主逻辑
# ======================
def check_all():

    d = get_all()

    p = d["pressure"]
    h = d["humidity"]
    ws = d["wind_speed"]
    wd = d["wind_dir"]
    aqi = d["aqi"]

    wind = ws > WIND_SPEED_THRESHOLD and NE_MIN <= wd <= NE_MAX
    pressure_low = p < PRESSURE_LOW
    humidity = h > HUMIDITY_THRESHOLD
    aqi_high = aqi >= AQI_THRESHOLD

    pressure_drop = calc_trend(TREND_PRESSURE_FILE, p, -PRESSURE_RATE_THRESHOLD)
    aqi_rise = calc_trend(TREND_AQI_FILE, aqi, AQI_DELTA_THRESHOLD)

    signals = {
        "wind": wind,
        "pressure": pressure_low,
        "humidity": humidity,
        "aqi": aqi_high
    }

    last = read_json(SIGNAL_STATE_FILE, {k:False for k in signals})
    count = sum(signals.values())

    if not should_run(count > 0):
        return

    msg = None
    now = time.time()

    # ======================
    # 单项
    # ======================
    if not last["humidity"] and humidity:
        msg = "🚨EnvAlert🚨\n✴️湿度🫧过高😶‍🌫️\n⛔️关闭新风▶️开除湿机"

    elif not last["pressure"] and pressure_low:
        msg = f"🚨气压过低 {p}"

    elif not last["wind"] and wind:
        msg = "🚨东北风触发"

    elif not last["aqi"] and aqi_high:
        msg = f"🚨高污染 AQI:{aqi}"

    # ======================
    # 趋势（保留）
    # ======================
    elif aqi_rise:
        msg = f"⚠️AQI快速上升 {aqi}"

    elif pressure_drop and wind:
        msg = "⚠️气压下降+东北风"

    # ======================
    # 分级预警（覆盖单项）
    # ======================
    if count == 2:
        msg = "🟡1️⃣级气象预警🚨"
    elif count == 3:
        msg = "🟠2️⃣级气象预警🚨"
    elif count >= 4:
        msg = "🔴3️⃣级气象预警🚨"

    # ======================
    # 全局恢复（12h）
    # ======================
    if count == 0 and any(last.values()):
        last_r = read_json(RECOVERY_FILE, {"t":0})["t"]
        if now - last_r > 43200:
            msg = "🟢EnvAlert恢复正常"
            save_json(RECOVERY_FILE, {"t": now})

    if msg:
        send(msg)

    save_json(SIGNAL_STATE_FILE, signals)

    print("气压:", p, "湿度:", h, "AQI:", aqi)
    print("风险数:", count)
