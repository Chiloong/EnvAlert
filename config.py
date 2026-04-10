import os

# ======================
# 🌍 数据源
# ======================
OPENWEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"
BARK_URL = "https://api.day.app"

# 🌫 WAQI（真实AQI）
WAQI_URL = "https://api.waqi.info/feed/geo:{lat};{lon}/?token={token}"
WAQI_TOKEN = os.environ.get("WAQI_TOKEN")

# ======================
# 📍 地点
# ======================
LAT = 35.21
LON = 113.29

# ======================
# 🔑 Secrets
# ======================
API_KEY = os.environ.get("API_KEY")
BARK_KEY = os.environ.get("BARK_KEY")

# ======================
# ⚖️ 阈值
# ======================

# 🌬 风
WIND_SPEED_THRESHOLD = 2.5
GUST_THRESHOLD = 4.0
NE_MIN = 20
NE_MAX = 100

# 🌡 气压
PRESSURE_LOW = 1000              # 🔴 低于触发
PRESSURE_RATE_THRESHOLD = 1.0    # 📉 每小时变化阈值

# 🌫 空气
AQI_THRESHOLD = 180              # 🔴 高污染
AQI_DELTA_THRESHOLD = 15         # 📈 快速上升

# ======================
# 📁 状态文件
# ======================
STATE_FILE = "fusion_state.txt"        # 总风险计数
PRESSURE_FILE = "pressure_state.txt"   # 气压趋势
AQI_STATE_FILE = "aqi_state.txt"       # AQI趋势
RECOVERY_FILE = "recovery_state.txt"   # 🟢 全局恢复节流
SIGNAL_STATE_FILE = "signal_state.txt" # ⭐ 信号级状态机（终极版核心）
