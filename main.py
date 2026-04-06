from wind import check_wind
from pressure import check_pressure
from fusion import check_fusion

def main():
    check_wind()
    check_pressure()
    check_fusion()   # ✅ 新增这一行

if __name__ == "__main__":
    main()
