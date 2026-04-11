def get_risk_color(risk):
    if risk < 30:
        return "🟢"
    elif risk < 60:
        return "🟡"
    elif risk < 80:
        return "🟠"
    else:
        return "🔴"


# =========================
# 🌏事件映射（统一语义）
# =========================
def map_event(e, data):

    if e == "wind_ne":
        return f"💨东北风"
    if e == "pressure_low":
        return f"🌨️气压低"
    if e == "aqi_high":
        return f"🌫️高污染"
    if e == "humidity_high":
        return f"🫧高湿度"
    if e == "pressure_change":
        return f"〽️气压变"

    return ""


# =========================
# 🔥智能合并核心
# =========================
def format_event(events, data, dp_level, risk):

    color = get_risk_color(risk)

    # 🟡等级
    if len(events) >= 4:
        level = "🔴3️⃣级气象预警🚨"
    elif len(events) == 3:
        level = "🟠2️⃣级气象预警🚨"
    elif len(events) == 2:
        level = "🟡1️⃣级气象预警🚨"
    else:
        level = "🟢单项气象预警"

    # 🔥事件压缩（关键）
    event_text = "".join([map_event(e, data) for e in events])

    # 📦严格4行
    return "\n".join([
        level,
        f"📉{dp_level}",
        f"🧠风险{color}{risk}/100",
        f"🌏环境异常组合：{event_text}"
    ])


def format_heartbeat(data, dp_level, risk):

    color = get_risk_color(risk)

    return "\n".join([
        "🌏EnvAlert☀️天气恢复正常✅",
        f"气压:{data['pressure']} 湿度:{data['humidity']}% 风:{data['wind_dir']} AQI:{data['aqi']}",
        f"📉{dp_level} 风险:{risk}{color}"
    ])
    
