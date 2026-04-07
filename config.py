import os

# 🌍 数据源配置
OPENWEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"
BARK_URL = "https://api.day.app"

# 📍 地点
LAT = 35.21
LON = 113.29

# 🔑 Secrets
API_KEY = os.environ.get("API_KEY")
BARK_KEY = os.environ.get("BARK_KEY")

# ⚖️ 阈值
PRESSURE_RATE_THRESHOLD = 1.0
WIND_SPEED_THRESHOLD = 2.5
GUST_THRESHOLD = 4.0
NE_MIN = 20
NE_MAX = 100

# 🔥 趋势阈值（新增）
TREND_PRESSURE_ACCEL_THRESHOLD = 0.5

# ⚙️ 状态文件
PRESSURE_STATE_FILE = "pressure_state.txt"
WIND_STATE_FILE = "wind_state.txt"
