def format_event(events, data, dp_level):

    lines = ["🚨EnvAlert🚨"]

    if "wind_ne" in events:
        lines.append(f"东北风{data['wind_scale']}级触发")

    if "pressure_low" in events:
        lines.append(f"气压过低{data['pressure']}hPa")

    if "aqi_high" in events:
        lines.append(f"高污染🌫️AQI{data['aqi']}")

    if "humidity_high" in events:
        lines.append(f"湿度过高{data['humidity']}%")

    if "pressure_low" in events or "wind_ne" in events:
        lines.append(f"⛔️环境干预建议")

    return "\n".join(lines[:4])


def format_heartbeat(data, dp_level, risk):
    return (
        "🌏EnvAlert☀️天气恢复正常✅\n"
        f"气压:{data['pressure']} 湿度:{data['humidity']}% 风:{data['wind_dir']} AQI:{data['aqi']}\n"
        f"ΔP:{dp_level} 风险:{risk}"
    )
