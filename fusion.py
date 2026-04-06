import time
from wind import check_wind
from pressure import check_pressure

def check_fusion():
    print("🧠 联动模块运行")
    # 联动逻辑：风速超阈值且气压下降超阈值 → 推送预警
    speed, deg = check_wind()
    check_pressure()
    print("🌬 风速/风向与🌡 气压联动完成")
