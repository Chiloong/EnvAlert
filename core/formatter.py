def get_risk_color(risk):
    if risk < 30:
        return "🟢"
    elif risk < 60:
        return "🟡"
    elif risk < 80:
        return "🟠"
    else:
        return "🔴"


def format_event(events, data, dp_level, risk):

    color = get_risk_color(risk)

    # ===== 映射 =====
    event_map = {
        "wind_ne": ("💨东北风", 1),
        "aqi_high": ("🌫️高污染", 2),
        "pressure_change": ("〽️气压变", 3),
        "pressure_low": ("🌨️气压低", 4),
        "humidity_high": ("🫧高湿度", 5),
    }

    # ===== 排序 + 拼接 =====
    event_list = []
    for e in events:
        if e in event_map:
            event_list.append(event_map[e])

    event_list = sorted(event_list, key=lambda x: x[1])
    event_text = "".join([e[0] for e in event_list])

    # ===== 级别 =====
    level = ""
    if len(events) >= 4:
        level = "🔴3️⃣级气象预警🚨"
    elif len(events) == 3:
        level = "🟠2️⃣级气象预警🚨"
    elif len(events) == 2:
        level = "🟡1️⃣级气象预警🚨"

    # ===== 单事件详情 =====
    lines = ["🚨EnvAlert🚨"]

    if "wind_ne" in events:
        lines.append(f"🏭东北风{data['wind_scale']}级💨")

    if "pressure_low" in events:
        lines.append(f"🌨️气压过低{data['pressure']}hPa")

    if "aqi_high" in events:
        lines.append(f"🌫️高污染AQI{data['aqi']}")

    if "humidity_high" in events:
        lines.append(f"🫧湿度{data['humidity']}%")

    lines.append(f"📉{dp_level} 🧠风险{color}{risk}/100")

    # ===== 组合输出（核心修复点）=====
    if level:
        return "\n".join([
            level,
            f"📉{dp_level}",
            f"🧠风险{color}{risk}/100",
            f"🌏环境异常组合：{event_text}"
        ])

    return "\n".join(lines[:4])


# 🔥补回 heartbeat（解决 ImportError）
def format_heartbeat(data, dp_level, risk):

    color = get_risk_color(risk)

    return (
        "🌏EnvAlert☀️天气恢复正常✅\n"
        f"气压{data['pressure']} 湿度{data['humidity']}% 风{data['wind_dir']} AQI{data['aqi']}\n"
        f"📉{dp_level} 🧠风险{color}{risk}/100"
    )
