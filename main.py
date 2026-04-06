from wind import check_wind
from pressure import check_pressure
from fusion import check_fusion   # ✅ 新增这一行

def main():
    check_wind()
    check_pressure()
    check_fusion()   # 联动分析，趋势判断

if __name__ == "__main__":
    main()
