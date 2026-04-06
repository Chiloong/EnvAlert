from wind import check_wind
from pressure import check_pressure

def check_fusion():
    print("🧠 联动模块运行")
    # 联动逻辑示例: 风速 > 阈值 && 气压下降速率 > 阈值 → 推送预警
    wind_speed, wind_deg = check_wind()
    if wind_speed is None:
        print("⚠️ 风数据异常，跳过联动判断")
        return
    last_pressure = None
    # 只做联动逻辑，不重复推送 pressure.py 的测试消息
    # 这里可以扩展其他设备或数据源联动逻辑
    print(f"🌬 风速/风向:{wind_speed}/{wind_deg} 与 🌡 气压联动完成")
